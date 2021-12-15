from sqlalchemy import Column, Boolean, Integer, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship, reconstructor


Base = declarative_base()

def initialize(dbname):
    engine = create_engine('sqlite:///' + dbname, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class DBMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Registry(DBMixin, Base):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    website = Column(String)
    flag = Column(Boolean, default=False)
    credentials = relationship("Credentials", back_populates="source")

    def __repr__(self):
        return f"<{self.website}(creation: {self.created_at}; update: {self.updated_at})>"


class Credentials(DBMixin, Base):
    cipher = Column(String, nullable=False)
    kdfsalt = Column(LargeBinary, nullable=False)
    ciphertext = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)
    mac = Column(LargeBinary, nullable=False)
    website_id = Column(Integer, ForeignKey("registry.id"))
    source = relationship("Registry", back_populates="credentials")

    def __repr__(self):
        return f"<Encrypted credentials for {self.source.website}>"


def list_all(session):
    query = session.query(Registry).filter(Registry.flag == False).order_by(Registry.website).all()
    print("ALL ENTRIES".center(40, '#'))
    for count, entry in enumerate(query):
        print(count, "-\t", entry.website)

def add_entry(session, new_entry):
    exists = session.query(Registry).filter(Registry.website == new_entry.website).exists()
    if exists == True:
        if input("Credentials for this website already exists. Do you want to update them? (y/n)").lower() == "y":
            #update_entry(session, new_entry)
            pass
    session.add(new_entry)

def read_entry(session, website):
    return session.query(Registry).filter(Registry.website == website).first()

def remove_entry(session, website):
    session.query(Registry).filter(Registry.website == website).delete()

def update_entry(session, website):
    # TODO
    pass
