import redis
from pymongo import MongoClient

# Connexion à MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["my_database"]
products = db["products"]

# Connexion à Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# Fonction pour récupérer les produits populaires
def get_popular_products():
    # Vérifier dans Redis
    cache = redis_client.get("popular_products")
    if cache:
        print("Données récupérées du cache Redis.")
        return cache

    # Si non trouvé, interroger MongoDB
    result = list(products.find({"popular": True}, {"_id": 0, "name": 1}))
    if result:
        redis_client.setex("popular_products", 60, str(result))  # TTL de 60 secondes
        print("Données récupérées de MongoDB et mises en cache.")
        return result

    print("Aucun produit populaire trouvé.")
    return []

# Fonction pour ajouter des produits dans MongoDB
def add_product(name, popular=False):
    product = {"name": name, "popular": popular}
    products.insert_one(product)
    print(f"Produit ajouté : {name} (popular={popular})")

# Exemple d'utilisation
if __name__ == "__main__":
    # Ajouter des produits pour l'exemple
    print("Ajout de produits...")
    add_product("Produit A", popular=True)
    add_product("Produit B", popular=False)
    add_product("Produit C", popular=True)

    # Récupérer les produits populaires (MongoDB -> Redis)
    print("\nPremière récupération (MongoDB) :")
    popular_products = get_popular_products()
    print("Produits populaires :", popular_products)

    # Récupérer à nouveau (Redis uniquement)
    print("\nDeuxième récupération (Redis) :")
    popular_products = get_popular_products()
    print("Produits populaires :", popular_products)
