# Geomix — Plataforma de Geometria Plana

Interface gamificada estilo Duolingo para aprendizagem de geometria plana.

## Conteúdo Pedagógico

| Unidade | Tema                         | Atividades |
|---------|------------------------------|------------|
| 1       | Identificação das Figuras    | 5 × 5 = 25 |
| 2       | Características das Figuras  | 5 × 5 = 25 |
| 3       | Fórmulas de Área             | 5 × 5 = 25 |
| 4       | Cálculo de Áreas             | 5 × 5 = 25 |
| 5       | Desafios Integradores        | 5 × 5 = 25 |

Total: 125 questões

### Tipos de exercício
- Múltipla escolha
- Arrastar e soltar
- Completar a resposta
- Jogo da memória
- Ordenar etapas
- Quiz cronometrado

## Melhorias do Plano de Melhoria (nov/2026)

| ID | Alteração |
|----|-----------|
| P-02 | Contraste ≥ 4,5:1 no perfil; textos maiores em Revisão, menu e perfil |
| P-04 | Campo de resposta com rótulo "Sua resposta" associado (`label for`) |
| P-05 | Resposta correta exibida após o erro em todos os tipos de exercício |
| P-06 | Trilha mostra uma unidade por tela (`/dashboard?unit=N`) |
| P-07 | Cartão "Continuar de onde parou" + rolagem até a atividade atual |
| P-08 | Botão Continuar no mesmo lugar do Verificar; feedback centralizado |
| P-09 | Perfil simplificado: progresso geral, status por unidade, acertos por categoria |
| P-10 | Triângulos visualmente distintos (qualquer × equilátero com marcas) |
| P-13 | Confirmação ao sair da atividade (✕) e ao sair da conta |
| P-14 | Guia "Como usar" curto e opcional |
| P-15 | Conquistas no perfil (calculadas do progresso; sem novos campos) |
| P-18 | H1 nas telas de exercício; links redundantes removidos |

## Como publicar (GitHub + Render + Firebase)

O Geomix é um app Flask (Python) que usa o **Firestore** como banco. O Firebase Hosting não roda Flask,
então o app é hospedado no **Render** (já configurado em `render.yaml`) e conversa com o Firestore.

### 1. GitHub
1. Crie um repositório e envie o conteúdo desta pasta (a raiz do repositório deve ter `app.py`, `render.yaml`, etc.).
2. Confira que `serviceAccountKey.json` **não** foi enviado (o `.gitignore` já bloqueia).

### 2. Firebase (Firestore)
1. No console do Firebase, abra o projeto → *Build → Firestore Database* e crie o banco, se ainda não existir.
2. *Configurações do projeto → Contas de serviço → Gerar nova chave privada* (baixa um `.json`).
3. (Opcional) publique as regras de bloqueio: `firebase deploy --only firestore:rules`.
   Coleções usadas: `users` e `progress` (criadas automaticamente).

### 3. Render
1. *New → Blueprint* (ou Web Service) apontando para o repositório do GitHub.
2. Em *Environment*, defina `FIREBASE_CREDENTIALS` com **todo o conteúdo** do `.json` da etapa 2.
   `SECRET_KEY` é gerada automaticamente.
3. Após o deploy, abra a URL do Render e teste.

### Rodar na sua máquina
`pip install -r requirements.txt`, salve a chave como `serviceAccountKey.json` na raiz e rode `python app.py`.
