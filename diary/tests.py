from django.test import TestCase
from django.core.management import call_command
import freezegun

from diary.models import Post, Tag


# Create your tests here.
class 新着タグ付与バッチ(TestCase):
  '''#4 バッチを自動テストする'''

  # テスト用データを投入する
  fixtures = ['diary/fixtures/tests/test_update_new_tag.json']

  def setUp(self):
    pass

  def tearDown(self):
    pass

  @freezegun.freeze_time('2021-06-09 13:00')
  def test_1(self):
    '''バッチを実行すると 1週間経過した記事 の新着タグが外れること'''
    call_command('update_new_tag')

    # 新着がついているが1週間経過した記事 を取得
    post = Post.objects.get(pk=1)
    self.assertEqual(0, len(post.tags.all()))

  @freezegun.freeze_time('2021-06-09 13:00')
  def test_2(self):
    '''バッチを実行すると 新着タグなし、1週間未経過記事 に新着タグがつくこと'''
    call_command('update_new_tag')

    # 新着タグなし、1週間未経過記事 を取得
    post = Post.objects.get(pk=2)
    self.assertEqual(1, len(post.tags.all()))
    # 新着タグがついている
    self.assertEqual('new', post.tags.first().slug)

  @freezegun.freeze_time('2021-06-09 13:00')
  def test_3(self):
    '''新着タグがDBにない場合に、バッチを実行したら...'''
    # 新着タグを全削除してからバッチ実行
    Tag.objects.all().delete()
    call_command('update_new_tag')

    # 新着タグなし、1週間未経過記事 を取得
    post = Post.objects.get(pk=2)
    self.assertEqual(1, len(post.tags.all()))
    # 自動で新着タグが生成され、付与されている
    self.assertEqual('new', post.tags.first().slug)

  @freezegun.freeze_time('2021-06-09 13:00')
  def test_4(self):
    '''新着タグをコマンドから指定できること'''
    call_command('update_new_tag', new_tag_slug='new2')

    # 新着タグなし、1週間未経過記事 を取得
    post = Post.objects.get(pk=2)
    self.assertEqual(1, len(post.tags.all()))
    # 指定した新着タグが生成され、付与されている
    self.assertEqual('new2', post.tags.first().slug)
