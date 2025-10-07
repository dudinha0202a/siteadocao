from ado_cao import create_app
from ado_cao.extensions import db
from ado_cao.models import User, Role, Animal
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_role = Role(name="admin")
    user_role = Role(name="user")
    db.session.add_all([admin_role, user_role])
    db.session.commit()

    admin = User(full_name="Admin AdoCão", email="admin@adocao.org")
    admin.set_password("admin123")
    admin.roles.append(admin_role)
    db.session.add(admin)

    a1 = Animal(name="Thor", species="cão", breed="SRD", age="2 anos", sex="macho",
                size="médio", city="Ariquemes", state="RO",
                description="Brincalhão, vacinado e castrado.",
                photo_url="https://images.unsplash.com/photo-1568572933382-74d440642117?q=80&w=1200&auto=format&fit=crop")
    a2 = Animal(name="Luna", species="gato", breed="Siamesa", age="1 ano", sex="fêmea",
                size="pequeno", city="Porto Velho", state="RO",
                description="Calma, gosta de carinho, vermifugada.",
                photo_url="https://images.unsplash.com/photo-1596854371257-0f14d8d7a6fe?q=80&w=1200&auto=format&fit=crop")
    db.session.add_all([a1, a2])

    db.session.commit()
    print("✅ Seed concluído. Admin: admin@adocao.org / senha: admin123")
