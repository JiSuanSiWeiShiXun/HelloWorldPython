# coding=utf-8
from flaskr import db

from sqlalchemy import Column, ForeignKey, Integer, String, Table, text, Identity
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(db.Model):
    __tablename__ = "user"
    name = Column(String(64), primary_key=True, nullable=False, comment=u"用户名称(primary_key)")
    info = Column(String(255), nullable=True, comment=u"用户信息") # 取出来是"" 还是空指针错误?

    objects = relationship("Object", back_populates="owner") # 与object构成一对多关系

    def __repr__(self):
        return f"User(name={self.name!r}, info={self.info!r})"


# 需求场景是物品管理器：想要录入冰箱里我需要的所有东西
class Object(db.Model):
    __tablename__ = "object"
    # id = Column(Interger, primary_key=True, nullable=False, autoincrement=True, comment=u"物品表主键")
    uid = Column(Integer, autoincrement=True, primary_key=True, nullable=False, comment=u"物品的全局唯一ID")
    name = Column(String(64), nullable=False, comment=u"物品名称")
    count = Column(Integer, nullable=False, server_default=text("1"), comment=u"物品数量")
    desc = Column(String(255), nullable=True, comment=u"物品信息")
    
    user_name = Column(String(64), ForeignKey("user.name"), nullable=False, comment=u"物品归属的用户ID")
    owner = relationship("User", back_populates="objects") # relationship貌似不影响表结构（除非多对多关系，需要创建中间表）

    def __repr__(self):
        return f"Object(id={self.uid}, name={self.name}, count={self.count}, owner={self.owner.name}, desc={self.desc})"

# NotifyUser = Table("notify_user", Base.metadata,
#     Column("notify_id", Integer, ForeignKey("notify.uid", ondelete="CASECADE"), primary_key=True),
#     Column("user_id", Integer, ForeignKey("user.uid", ondelete="CASECADE"), primary_key=True),
# )

# # notify: 提醒我某些食物要过期了，提醒某些东西长期闲置并未使用
# # 感觉这么设置没什么意义，应该给object设置一个字段为类别，在user表中设置一个realtion为需要定期提醒的物品
# class Notify(db.Model):
#     __tablename__ = "notify"
#     uid = Column(Integer, autoincrement=True, primary_key=True, nullable=False, comment=u"主键id")
#     notify_desc = Column(String(64), nullable=True, comment=u"通知简介")
#     user_list = relationship("User", secondary=NotifyUser, backref="notify") # notify:user 必须要foreignKey 或者 中间表 才能创建表之间的关系 

