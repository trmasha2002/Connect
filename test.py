from web import db
from web.models.idea import Idea
from web.models.user import User

# user = User("trmasha2015@yandex.ru", "trmasha2002", "tr3088848")
# user.save()
# user2 = User("trmasha2002@yandex.ru", "trmasha2018", "123456")
# user2.save()
# idea = Idea("me", "me", "me", "me")
# idea.author_id = 1
# idea.save()
# idea = Idea("me2", "me2", "me2", "me2")
# idea.author_id = 1
# idea.save()
# idea = Idea("me3", "me3", "me3", "me3")
# idea.author_id = 1
# idea.save()
#
# idea.subscritions.append(user)
# idea.subscritions.append(user2)
# db.session.add(idea)
# db.session.commit()


print(Idea.get_by_id(3).subscritions)
