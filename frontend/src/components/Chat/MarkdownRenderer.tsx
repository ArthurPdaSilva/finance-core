"use client";
import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";

type MarkdownRendererProps = {
  markdown: string;
};

export function MarkdownRenderer({ markdown }: MarkdownRendererProps) {
  return (
    // Removido 'prose-invert' e ajustado cores para o tema claro
    <div className="prose prose-slate w-full max-w-none overflow-hidden lg:prose-lg prose-th:text-[#167EAC] prose-td:text-gray-700">
      <ReactMarkdown
        rehypePlugins={[rehypeSanitize]}
        remarkPlugins={[remarkGfm]}
        components={{
          li: ({ node, ...props }) => (
            <li className="[&>p]:mb-0 [&>p]:inline" {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul
              className="list-disc list-outside ml-6 mb-2 mt-2 last:mb-0 space-y-1"
              {...props}
            />
          ),
          table: ({ node, ...props }) => (
            // Fundo branco sólido ou levemente cinza para destacar do balão
            <div className="my-4 w-full overflow-x-auto rounded-lg border border-gray-200 bg-gray-50/50">
              <table
                className="w-full border-collapse text-left text-sm"
                {...props}
              />
            </div>
          ),
          thead: ({ node, ...props }) => (
            <thead
              className="bg-gray-100 uppercase font-bold text-[10px] tracking-wider"
              {...props}
            />
          ),
          tbody: ({ node, ...props }) => (
            <tbody className="divide-y divide-gray-200" {...props} />
          ),
          tr: ({ node, ...props }) => (
            <tr className="hover:bg-white transition-colors" {...props} />
          ),
          th: ({ node, ...props }) => (
            <th
              className="px-4 py-3 border-b border-gray-200 text-base"
              {...props}
            />
          ),
          td: ({ node, ...props }) => <td className="px-4 py-3" {...props} />,
          p: ({ node, ...props }) => (
            <p className="mb-4 last:mb-0 leading-relaxed" {...props} />
          ),
          h2: ({ node, ...props }) => (
            <h2 className="text-2xl font-bold mb-4 text-gray-800" {...props} />
          ),
          h3: ({ node, ...props }) => (
            <h3 className="text-xl font-bold mb-4 text-gray-800" {...props} />
          ),
          hr: ({ node, ...props }) => (
            <hr className="my-4 border-gray-200" {...props} />
          ),
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
}
