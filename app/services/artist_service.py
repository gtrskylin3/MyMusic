from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Form
from app.auth import utils
from app.models import Artist
from app.repositories.artists import artist_repository
from app.schemas.artists import ArtistCreate, ArtistRead, ArtistScheme


class ArtistService:
    async def create_artist(self, db: AsyncSession, *, artist_in: ArtistCreate) -> ArtistRead:
        # 1. Проверяем, существует ли пользователь
        existing_artist = await artist_repository.get_by_username(db, username=artist_in.username)
        if existing_artist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artist with this username already exists",
            )

        # 2. Готовим данные для сохранения в БД
        genres = artist_in.genres
        create_data = artist_in.model_dump(exclude={'genres'})

        # 3. Хешируем пароль и заменяем поле
        hashed_password = utils.hash_password(artist_in.password)
        create_data.pop("password")  # Удаляем пароль в открытом виде
        create_data["hash_password"] = hashed_password  # Добавляем хеш

        # 4. Передаем в репозиторий чистые данные
        artist = await artist_repository.create(db, genres, artist_data=create_data)
        return ArtistRead.model_validate(artist)
        
    async def get_artist_by_id(self, db: AsyncSession, artist_id: int) -> ArtistRead:
        artist = await artist_repository.get_by_id(db, artist_id)
        if not artist:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail=f"Artist with id {artist_id} not found"
            )
        return ArtistRead.model_validate(artist)


    async def get_artist_by_username(self, db: AsyncSession, username: str) -> ArtistRead:
        artist = await artist_repository.get_by_username(db, username)
        if not artist:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"Artist with username {username} not found",
            )
        return ArtistRead.model_validate(artist)

    async def validate_artist_credentials(
        self, db: AsyncSession, username: str = Form(), password: str = Form()
    ) -> ArtistScheme:
        """
        Валидирует artistname и password при логине.

        Args:
            artistname: Имя пользователя из формы
            password: Пароль из формы

        Returns:
            ArtistScheme: Аутентифицированный пользователь

        Raises:
            HTTPException: Если credentials неверны или пользователь неактивен
        """
        artist = await artist_repository.get_by_username(db, username)

        if not artist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not utils.validate_password(password, artist.hash_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not artist.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Artist account is inactive"
            )

        return ArtistScheme.model_validate(artist)


artist_service = ArtistService()
