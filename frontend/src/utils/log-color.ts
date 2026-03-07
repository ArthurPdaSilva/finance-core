import { styleText } from "node:util";

export function logColor(...msg: (string | number)[]) {
  const messages = msg
    .map((message) => styleText(["bgGreen", "whiteBright"], `${message}`))
    .join(" ");
  console.log(styleText("green", messages));
}
