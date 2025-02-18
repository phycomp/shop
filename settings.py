DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop',
        'USER': 'postgres',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS = [
#...,
    'rest_framework',
    'corsheaders',
    'shop',
    'api'
]

# 添加 CORS 配置
CORS_ALLOW_ALL_ORIGINS = True  # 開發時可暫時允許所有域名

# DRF 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}
