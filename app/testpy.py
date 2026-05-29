# from sqlalchemy import (
#     ForeignKey,
#     MetaData,
#     Table,
#     create_engine,
#     String,
#     Integer,
#     Boolean,
#     Float,
#     func,
#     select
# )

# from sqlalchemy.orm import (
#     DeclarativeBase,
#     Mapped,
#     mapped_column,
#     relationship,
#     sessionmaker
# )


# # =========================
# # CONFIG DATABASE
# # =========================

# # sqlite:///test.db
# # sqlite база буде створена в файлі test.db

# engine = create_engine(
#     "sqlite:///test.db",

#     # показувати SQL у консолі
#     # echo=True,

#     # майбутній стиль SQLAlchemy 2.0
#     future=True
# )


# # =========================
# # BASE CLASS
# # =========================

# class Base(DeclarativeBase):
#     pass


# # =========================
# # MODEL
# # =========================

# class User(Base):
#     __tablename__ = "users"

#     # PRIMARY KEY
#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         autoincrement=True
#     )

#     # NOT NULL
#     name: Mapped[str] = mapped_column(
#         String(50),
#         nullable=False
#     )

#     # UNIQUE
#     email: Mapped[str] = mapped_column(
#         String(100),
#         unique=True
#     )

#     # DEFAULT VALUE
#     is_active: Mapped[bool] = mapped_column(
#         Boolean,
#         default=True
#     )

#     # FLOAT
#     salary: Mapped[float] = mapped_column(
#         Float,
#         default=0
#     )

#     products: Mapped[list["Product"]] = relationship(back_populates="user")

#     def __repr__(self):
#         return (
#             f"User("
#             f"id={self.id}, "
#             f"name='{self.name}', "
#             f"email='{self.email}', "
#             f"is_active={self.is_active}, "
#             f"salary={self.salary}"
#             f")"
#         )

# class Product(Base):
#     __tablename__ = "products"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#     price: Mapped[float] = mapped_column(Float, default=0)
#     is_available: Mapped[bool] = mapped_column(Boolean, default=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["User"] = relationship(back_populates="products")
    
#     def __repr__(self):
#         return f"Product(id={self.id}, name='{self.name}', price={self.price})"
# # =========================
# # CREATE TABLES
# # =========================

# Base.metadata.create_all(engine)


# # =========================
# # SESSION FACTORY
# # =========================

# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False
# )


# # =========================
# # INSERT DATA
# # =========================

# # with SessionLocal() as session:

# #     user1 = User(
# #         name="Illia",
# #         email="illia@gmail.com",
# #         salary=2500
# #     )

# #     user2 = User(
# #         name="Maks",
# #         email="maks@gmail.com",
# #         is_active=False,
# #         salary=1800
# #     )

# #     session.add(user1)
# #     session.add(user2)

# #     session.commit()

# # with SessionLocal() as session:
# #     product1 = Product(
# #         name="Laptop",
# #         price=1500.0,
# #         user_id=1
# #     )
# #     product2 = Product(
# #         name="Phone",
# #         price=800.0,
# #         user_id=1
# #     )

# #     session.add(product1)
# #     session.add(product2)
# #     session.commit()

# # =========================
# # SELECT DATA
# # =========================

# # with SessionLocal() as session:
# #     users = [
# #         User(name="Anna", email="anna@gmail.com", salary=3200, is_active=True),
# #         User(name="Bohdan", email="bohdan@gmail.com", salary=900, is_active=False),
# #         User(name="Daria", email="daria@gmail.com", salary=4500, is_active=True),
# #         User(name="Petro", email="petro@gmail.com", salary=1200, is_active=True),
# #     ]
# #     session.add_all(users)
# #     session.commit()


# with SessionLocal() as session:
#     stmt = (
#     select(User.name, func.sum(Product.price).label("count"))
#     .join(Product, User.id == Product.user_id)
#     .group_by(User.name)
#     .having(func.sum(Product.price) >= 1)
#     )
    
#     print(stmt)

# with SessionLocal() as session:
#     result = session.execute(stmt).all()
#     for name, count in result:
#         print(f"{name}: {count}")