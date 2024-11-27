from Database import SocialScoreDatabase

def main():
    db = SocialScoreDatabase("neo4j://localhost:7687", "neo4j", "password")

    while True:
        print("\n=== Rede Social ===")
        print("1. Criar Usuário")
        print("2. Avaliar Usuário")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            login = input("Digite o login do usuário: ")
            senha = input("Digite a senha do usuário: ")
            db.criar_usuario(login, senha)
            print(f"Usuário {login} criado com sucesso!")

        elif choice == '2':
            avaliador = input("Digite o login do avaliador: ")
            avaliado = input("Digite o login do avaliado: ")

            if not db.usuario_existe(avaliador):
                print(f"Usuário {avaliador} não encontrado.")
                continue
            if not db.usuario_existe(avaliado):
                print(f"Usuário {avaliado} não encontrado.")
                continue

            try:
                nota = float(input("Digite a nota (0 a 5): "))
                if nota < 0 or nota > 5:
                    print("Nota deve estar entre 0 e 5.")
                    continue
            except ValueError:
                print("Por favor, insira um número válido para a nota.")
                continue

            contexto = input("Digite o contexto da avaliação: ")
            db.avaliar_usuario(avaliador, avaliado, nota, contexto)
            print(f"{avaliador} avaliou {avaliado} com a nota {nota} no contexto: '{contexto}'.")

        elif choice == '3':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    db.close()


if __name__ == "__main__":
    main()