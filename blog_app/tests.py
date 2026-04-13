from django.test import TestCase, Client
from django.urls import reverse
from .models import Post
from .forms import PostForm

class PostModelTest(TestCase):
    """Тесты для модели Post"""
    
    def setUp(self):
        """Создаем тестовый пост"""
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Это содержание тестового поста для проверки'
        )
    
    def test_post_creation(self):
        """Тест создания поста"""
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertEqual(self.post.content, 'Это содержание тестового поста для проверки')
        self.assertTrue(isinstance(self.post, Post))
    
    def test_post_str_method(self):
        """Тест метода __str__"""
        self.assertEqual(str(self.post), 'Тестовый пост')

class PostViewsTest(TestCase):
    """Тесты для представлений (views)"""
    
    def setUp(self):
        """Создаем тестовые данные"""
        self.client = Client()
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержание тестового поста'
        )
    
    def test_home_page_status_code(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/home.html')
    
    def test_post_list_page_status_code(self):
        """Тест страницы списка постов"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/posts.html')
    
    def test_post_detail_page_status_code(self):
        """Тест страницы отдельного поста"""
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/post_detail.html')
    
    def test_post_detail_page_contains_post_data(self):
        """Тест: страница поста содержит правильные данные"""
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
    
    def test_about_page_status_code(self):
        """Тест страницы 'О себе'"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/about.html')
    
    def test_post_create_page_status_code(self):
        """Тест страницы создания поста"""
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/create_post.html')

class PostURLsTest(TestCase):
    """Тесты для маршрутов (URLs)"""
    
    def setUp(self):
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержание тестового поста'
        )
    
    def test_home_url(self):
        """Тест URL главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_posts_list_url(self):
        """Тест URL списка постов"""
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_url(self):
        """Тест URL детальной страницы поста"""
        response = self.client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_create_url(self):
        """Тест URL создания поста"""
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_url(self):
        """Тест URL страницы 'О себе'"""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_nonexistent_post_returns_404(self):
        """Тест: несуществующий пост возвращает 404"""
        response = self.client.get('/posts/99999/')
        self.assertEqual(response.status_code, 404)

class PostFormTest(TestCase):
    """Тесты для формы создания/редактирования поста"""
    
    def test_valid_form(self):
        """Тест валидной формы"""
        form_data = {
            'title': 'Новый пост',
            'content': 'Это содержание нового поста для теста'
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_empty_title(self):
        """Тест: пустой заголовок - форма невалидна"""
        form_data = {
            'title': '',
            'content': 'Содержание поста'
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_invalid_form_short_title(self):
        """Тест: слишком короткий заголовок (< 3 символов)"""
        form_data = {
            'title': '12',
            'content': 'Содержание поста для теста'
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_invalid_form_short_content(self):
        """Тест: слишком короткое содержание (< 10 символов)"""
        form_data = {
            'title': 'Новый пост',
            'content': 'Коротко'
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

class PostCreateAndEditTest(TestCase):
    """Тесты для создания и редактирования постов"""
    
    def setUp(self):
        self.client = Client()
    
    def test_create_post_via_form(self):
        """Тест создания поста через форму"""
        post_data = {
            'title': 'Созданный пост',
            'content': 'Это содержание созданного через форму поста'
        }
        response = self.client.post(reverse('post_create'), post_data)
        
        # Проверяем, что пост создался
        self.assertEqual(Post.objects.count(), 1)
        
        # Проверяем, что произошло перенаправление
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Проверяем данные созданного поста
        created_post = Post.objects.first()
        self.assertEqual(created_post.title, 'Созданный пост')
        self.assertEqual(created_post.content, 'Это содержание созданного через форму поста')
    
    def test_update_post_via_form(self):
        """Тест редактирования поста через форму"""
        post = Post.objects.create(
            title='Старый заголовок',
            content='Старое содержание'
        )
        
        updated_data = {
            'title': 'Новый заголовок',
            'content': 'Новое содержание'
        }
        
        response = self.client.post(reverse('post_edit', args=[post.pk]), updated_data)
        
        # Проверяем, что произошло перенаправление
        self.assertEqual(response.status_code, 302)
        
        # Обновляем пост из базы
        post.refresh_from_db()
        self.assertEqual(post.title, 'Новый заголовок')
        self.assertEqual(post.content, 'Новое содержание')
    
    def test_delete_post(self):
        """Тест удаления поста"""
        post = Post.objects.create(
            title='Пост для удаления',
            content='Содержание поста для удаления'
        )
        
        self.assertEqual(Post.objects.count(), 1)
        
        response = self.client.post(reverse('post_delete', args=[post.pk]))
        
        # Проверяем перенаправление
        self.assertEqual(response.status_code, 302)
        
        # Проверяем, что пост удален
        self.assertEqual(Post.objects.count(), 0)

