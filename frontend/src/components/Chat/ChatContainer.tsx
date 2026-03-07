type ChatContainerProps = {
  children: React.ReactNode;
};

export const ChatContainer = ({ children }: ChatContainerProps) => {
  return (
    <div className="bg-gray-200 h-screen flex flex-col flex-1 gap-5">
      {children}
    </div>
  );
};
