# Avatar Theo – 8 anos 🔥🌪️🪨💧

Convite com confirmação de presença (GitHub Pages + Firebase).

- `index.html`: convite e formulário, o link que vai para os convidados
- `painel.html`: lista e totais, que só abre com login Google autorizado
- `firebase-config.js`: configuração do Firebase e e-mails do painel
- `firestore.rules`: regras de segurança (convidado só grava; só você lê)

## Configuração

1. **Firebase** (console.firebase.google.com): use um projeto existente ou crie um.
   - *Firestore Database*: crie o banco, se ainda não tiver.
   - *Authentication > Sign-in method*: ative **Google**.
   - *Authentication > Settings > Authorized domains*: adicione `thiagovinicius7.github.io`.
   - *Firestore > Regras*: cole o conteúdo de `firestore.rules` e publique.
     Se o projeto já tiver regras para outros apps, cole só o bloco `match /festaTheo8/{id}`
     e as duas funções dentro das regras existentes.
2. **firebase-config.js**: cole a config do app Web (Configurações do projeto > Seus apps).
3. **GitHub**: crie o repositório `festa-theo` (público) e suba os 4 arquivos.
   Depois vá em *Settings > Pages > Branch: main / root*.

## Links

- Convidados: `https://thiagovinicius7.github.io/festa-theo/`
- Seu painel: `https://thiagovinicius7.github.io/festa-theo/painel.html`

Se a mesma pessoa confirmar de novo com o mesmo nome, a resposta é atualizada e não duplica.
Para liberar o painel para outra pessoa, adicione o e-mail dela em `firebase-config.js`
**e** em `firestore.rules`.
