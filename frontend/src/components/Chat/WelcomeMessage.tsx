type WelcomeMessageProps = {
  hidden: boolean;
};

export const WelcomeMessage = ({ hidden }: WelcomeMessageProps) => {
  if (hidden) return;

  return (
    <div className="flex self-start max-w-[80%] md:max-w-[60%] bg-white p-4 rounded-2xl rounded-tl-none shadow-sm">
      <p className="text-sm md:text-base font-medium text-gray-700">
        Olá! Eu sou o Finance Bot e estou aqui para te ajudar com suas finanças
        :)
      </p>
    </div>
  );
};
