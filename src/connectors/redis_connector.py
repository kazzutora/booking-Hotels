import redis.asyncio as redis
from typing import Optional, Any


class RedisManager:
    """Асинхронный менеджер для работы с Redis"""

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None):
        """
        Инициализация менеджера Redis

        Args:
            host: Хост Redis сервера
            port: Порт Redis сервера
            db: Номер базы данных
            password: Пароль для подключения (если требуется)
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client: Optional[redis.Redis] = None

    async def __aenter__(self):
        """Асинхронный контекстный менеджер для входа"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер для выхода"""
        await self.disconnect()

    async def connect(self):
        """Асинхронное подключение к Redis (без пароля)"""
        try:
            self.client = await redis.from_url(
                f"redis://{self.host}:{self.port}/{self.db}",
                decode_responses=True
            )
            # Проверяем подключение
            await self.client.ping()
            print(f"Успешно подключено к Redis на {self.host}:{self.port}")
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
            raise

    async def disconnect(self):
        """Асинхронное отключение от Redis"""
        if self.client:
            await self.client.close()
            print("Отключено от Redis")

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """
        Установка значения по ключу

        Args:
            key: Ключ
            value: Значение (будет преобразовано в строку)
            expire: Время жизни ключа в секундах (опционально)

        Returns:
            bool: True если успешно, иначе False
        """
        if not self.client:
            raise ConnectionError("Не установлено подключение к Redis")

        try:
            if expire:
                await self.client.setex(key, expire, str(value))
            else:
                await self.client.set(key, str(value))
            return True
        except Exception as e:
            print(f"Ошибка при установке значения для ключа '{key}': {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        """
        Получение значения по ключу

        Args:
            key: Ключ

        Returns:
            Optional[str]: Значение или None если ключ не найден
        """
        if not self.client:
            raise ConnectionError("Не установлено подключение к Redis")

        try:
            value = await self.client.get(key)
            return value
        except Exception as e:
            print(f"Ошибка при получении значения для ключа '{key}': {e}")
            return None

    async def delete(self, key: str) -> bool:
        """
        Удаление ключа

        Args:
            key: Ключ для удаления

        Returns:
            bool: True если ключ был удален, False если не найден или ошибка
        """
        if not self.client:
            raise ConnectionError("Не установлено подключение к Redis")

        try:
            result = await self.client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Ошибка при удалении ключа '{key}': {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Проверка существования ключа

        Args:
            key: Ключ для проверки

        Returns:
            bool: True если ключ существует
        """
        if not self.client:
            raise ConnectionError("Не установлено подключение к Redis")

        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            print(f"Ошибка при проверке существования ключа '{key}': {e}")
            return False


# Пример использования
async def main():
    # Использование с контекстным менеджером (рекомендуемый способ)
    async with RedisManager(host='localhost', port=6379, db=0) as redis_mgr:
        # Установка значения с истечением через 60 секунд
        await redis_mgr.set('user:1', 'Alice', expire=60)

        # Получение значения
        user = await redis_mgr.get('user:1')
        print(f"Получено значение: {user}")

        # Проверка существования
        exists = await redis_mgr.exists('user:1')
        print(f"Ключ существует: {exists}")

        # Удаление ключа
        await redis_mgr.delete('user:1')

        # Проверка после удаления
        user_after = await redis_mgr.get('user:1')
        print(f"Значение после удаления: {user_after}")

    # Альтернативный способ: ручное подключение/отключение
    redis_mgr = RedisManager(host='localhost', port=6379, db=0)
    await redis_mgr.connect()
    try:
        await redis_mgr.set('test', 'value', expire=30)
        value = await redis_mgr.get('test')
        print(f"Значение: {value}")
    finally:
        await redis_mgr.disconnect()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())