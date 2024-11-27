from Database import SocialScoreDatabase

if __name__ == "__main__":
    db = SocialScoreDatabase("neo4j://localhost:7687", "neo4j", "password")

    db.criar_usuario("Alice", 30)
    db.criar_usuario("Bob", 25)

    db.avaliar_usuario("Alice", "Bob", 4.5, "Social interaction")
    db.avaliar_usuario("Bob", "Alice", 3.8, "Work-related interaction")


    db.close()
