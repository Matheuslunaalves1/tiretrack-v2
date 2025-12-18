// Pequeno helper `cn` (class names) usado pela UI.
// Garante compatibilidade com imports '@/lib/utils'.
export function cn(...inputs: Array<string | false | null | undefined | Record<string, boolean>>): string {
  const classes: string[] = [];
  for (const item of inputs) {
    if (!item) continue;
    if (typeof item === 'string') {
      classes.push(item);
    } else if (typeof item === 'object') {
      for (const [key, value] of Object.entries(item)) {
        if (value) classes.push(key);
      }
    }
  }
  return classes.join(' ');
}

export default cn;
