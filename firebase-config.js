// Cole aqui a configuração do seu app Web do Firebase
// (Console do Firebase > Configurações do projeto > Seus apps > SDK setup > Config)
export const firebaseConfig = {
  apiKey: "AIzaSyAgr7MKgTeja8hCbkhPbVy70WB6fYDqb1Y",
  authDomain: "festa-theo-3f43d.firebaseapp.com",
  projectId: "festa-theo-3f43d",
  storageBucket: "festa-theo-3f43d.firebasestorage.app",
  messagingSenderId: "212818985669",
  appId: "1:212818985669:web:4cf37da7b21e62793e26ac"
};

// Quem pode abrir o painel (tem que ser igual ao que está em firestore.rules)
export const EMAILS_PAINEL = ["thiagovinicius7@gmail.com"];

// Coleção no Firestore
export const COLECAO = "festaTheo8";

// Onde fica a foto da capa trocada pelo painel
export const COLECAO_CONFIG = "festaTheo8Config";
