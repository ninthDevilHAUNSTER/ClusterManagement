# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Software(Base):
    __tablename__ = 'software'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)


class SoftwareVersion(Base):
    __tablename__ = 'software_version'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    version = Column(String(100), nullable=False)
    fk_software_id = Column(ForeignKey('software.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                            index=True)

    software = relationship('Software')


class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    cve = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    fk_software_id = Column(ForeignKey('software.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                            index=True)
    vuln_type = Column(String(50))
    poc_url = Column(String(400))
    patch_url = Column(String(400))
    patched_versions = Column(String(400))
    select_version = Column(String(50))

    software = relationship('Software')


class Test(Base):
    __tablename__ = 'tests'

    id = Column(INTEGER(11), primary_key=True, unique=True, autoincrement=True)
    test_name = Column(String(100), server_default=text("'unnamed'"))
    test_group = Column(String(250), nullable=False, index=True, server_default=text("'default'"))
    test_date = Column(DateTime, index=True)
    fk_software_id = Column(ForeignKey('software.id', ondelete='CASCADE', onupdate='CASCADE'), index=True,
                            server_default=text("0"))
    fk_software_version_id = Column(ForeignKey('software_version.id', ondelete='CASCADE', onupdate='CASCADE'),
                                    index=True, server_default=text("0"))
    test_data = Column(LONGTEXT)
    request_hash = Column(String(100), server_default=text("'0000000000000000000000000000000000000000'"))

    software = relationship('Software')
    software_version = relationship('SoftwareVersion')


class VulnerabilitySoftware(Base):
    __tablename__ = 'vulnerability_software'

    id = Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    fk_version_id = Column(ForeignKey('software_version.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                           nullable=False, index=True)
    fk_vulnerability_id = Column(ForeignKey('vulnerabilities.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 primary_key=True, nullable=False, index=True)

    version = relationship('SoftwareVersion')
    vulnerability = relationship('Vulnerability')


class CoveredFile(Base):
    __tablename__ = 'covered_files'

    id = Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    file_name = Column(String(400), primary_key=True, nullable=False, index=True)
    fk_test_id = Column(ForeignKey('tests.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    test = relationship('Test')


class IncludedFile(Base):
    __tablename__ = 'included_files'

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    file_name = Column(VARCHAR(400), nullable=False, index=True)
    fk_test_id = Column(ForeignKey('tests.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    test = relationship('Test')


class VulnerableFile(Base):
    __tablename__ = 'vulnerable_files'

    id = Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    file_name = Column(String(250), primary_key=True, nullable=False)
    fk_vulnerability_software = Column(ForeignKey('vulnerability_software.id', ondelete='CASCADE', onupdate='CASCADE'),
                                       primary_key=True, nullable=False, index=True)

    vulnerability_software = relationship('VulnerabilitySoftware')


class CoveredLine(Base):
    __tablename__ = 'covered_lines'

    id = Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    line_number = Column(INTEGER(11), primary_key=True, nullable=False, index=True)
    run = Column(INTEGER(11), nullable=False)
    fk_file_id = Column(ForeignKey('covered_files.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    file = relationship('CoveredFile')


class VulnerableLine(Base):
    __tablename__ = 'vulnerable_lines'

    id = Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    line_number = Column(INTEGER(11), primary_key=True, nullable=False)
    fk_vulnerability_software = Column(ForeignKey('vulnerability_software.id', ondelete='CASCADE', onupdate='CASCADE'),
                                       primary_key=True, nullable=False, index=True)
    fk_vulnerable_file = Column(ForeignKey('vulnerable_files.id', ondelete='CASCADE', onupdate='CASCADE'),
                                primary_key=True, nullable=False, index=True)

    vulnerability_software = relationship('VulnerabilitySoftware')
    vulnerable_file = relationship('VulnerableFile')


from sqlalchemy import create_engine, MetaData


def create_database(user="root",
                    password="password",
                    host="websec",
                    port="21305",
                    database="code_coverage", ):
    socket_word = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(socket_word)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()
