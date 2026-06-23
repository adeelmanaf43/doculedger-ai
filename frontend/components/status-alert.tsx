type StatusAlertProps = {
  title?: string;
  message: string;
  tone?: "info" | "success" | "warning" | "error";
};

const toneStyles = {
  info: "border-line bg-white text-ink",
  success: "border-teal-200 bg-teal-50 text-teal-950",
  warning: "border-amber-200 bg-amber-50 text-amber-950",
  error: "border-rose-200 bg-rose-50 text-rose-950",
};

export function StatusAlert({
  title,
  message,
  tone = "info",
}: StatusAlertProps) {
  return (
    <div className={`rounded-lg border px-4 py-3 ${toneStyles[tone]}`}>
      {title ? <p className="text-sm font-semibold">{title}</p> : null}
      <p className="mt-1 text-sm leading-6">{message}</p>
    </div>
  );
}
