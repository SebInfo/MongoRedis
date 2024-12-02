import redis

# Connexion au serveur Redis
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Filtrage des utilisateurs avec age > 25
def filter_users_by_age(min_age):
    # Récupérer toutes les clés correspondant au motif 'user:*'
    keys = client.keys("user:*")
    result = []

    for key in keys:
        # Récupérer le champ 'age' pour chaque utilisateur
        age = client.hget(key, "age")
        if age and int(age) > min_age:  # Vérifier si l'âge est supérieur au seuil
            # Ajouter la clé et ses données filtrées au résultat
            user_data = client.hgetall(key)  # Récupérer toutes les données de l'utilisateur
            result.append(user_data)

    return result

# Appel de la fonction pour trouver les utilisateurs ayant un âge > 25
filtered_users = filter_users_by_age(25)

# Afficher les résultats
for user in filtered_users:
    print(user)
