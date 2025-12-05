export const users = [
  {
    name: "Jesús De La O",
    email: "jesus@icc.com",
    password: "jesus",
    rol: "admin",
  },
  {
    name: "Cliente Demo",
    email: "cliente@icc.com",
    password: "cliente",
    rol: "cliente",
  },
];

export function loginDemo(email, password) {
  return users.find(
    (u) => u.email.toLowerCase() === email.toLowerCase() && u.password === password
  );
}
