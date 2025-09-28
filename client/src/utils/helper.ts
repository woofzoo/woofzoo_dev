const getOptions = (types: any): { value: string; label: string }[] => {
   let list: any[] = [];

   if (Array.isArray(types)) {
      list = types;
   } else if (
      types &&
      typeof types === "object" &&
      Array.isArray((types as any).types)
   ) {
      list = (types as any).types;
   }

   const humanize = (s: string) => {
      if (!s) return "";
      const str = String(s).toLowerCase().replace(/_/g, " ");
      return str.charAt(0).toUpperCase() + str.slice(1);
   };

   return list.map((t) => {
      if (!t) return { value: String(t), label: "" };
      if (typeof t === "string") return { value: t, label: humanize(t) };
      if (typeof t === "object" && (t.value || t.label)) {
         return {
            value: t.value ?? t.id ?? String(t),
            label: t.label ?? humanize(t.value ?? t.id ?? String(t)),
         };
      }
      return { value: String(t), label: humanize(String(t)) };
   });
};
