export const COLORS = {
  // === COLORES PRINCIPALES POSITIVA ===
  primary: "#F58220",           // Naranja POSITIVA (principal)
  primaryHover: "#E5721A",      // Naranja oscuro (hover)
  primaryLight: "#FEF3E8",      // Naranja muy claro (backgrounds)
  primaryMuted: "#F5822033",    // Naranja con transparencia

  // === COLORES SECUNDARIOS ===
  secondary: "#1E293B",         // Azul oscuro/slate (sidebar, headers)
  secondaryLight: "#334155",    // Slate medio
  secondaryMuted: "#64748B",    // Slate para textos secundarios

  // === COLORES DE ESTADO ===
  success: "#22C55E",           // Verde éxito
  successLight: "#DCFCE7",
  warning: "#F59E0B",           // Amarillo advertencia
  warningLight: "#FEF3C7",
  danger: "#EF4444",            // Rojo error
  dangerLight: "#FEE2E2",
  info: "#3B82F6",              // Azul información
  infoLight: "#DBEAFE",

  // === NEUTROS ===
  white: "#FFFFFF",
  background: "#F8FAFC",        // Gris muy claro (fondo principal)
  surface: "#FFFFFF",           // Blanco (tarjetas)
  border: "#E2E8F0",            // Bordes
  text: "#0F172A",              // Texto principal
  textMuted: "#64748B",         // Texto secundario
  textLight: "#94A3B8",         // Texto terciario
} as const;

// Colores para gráficos
export const CHART_COLORS = [
  "#F58220",  // Naranja POSITIVA
  "#3B82F6",  // Azul
  "#22C55E",  // Verde
  "#F59E0B",  // Amarillo
  "#8B5CF6",  // Púrpura
  "#EC4899",  // Rosa
  "#14B8A6",  // Teal
  "#F97316",  // Naranja claro
];

// Menú de navegación
export const MENU_ITEMS = [
  { name: "Dashboard", href: "/", icon: "LayoutDashboard" },
  { name: "Consolidador T25", href: "/consolidador", icon: "Settings2" },
  { name: "Explorador FTP", href: "/explorador", icon: "FolderOpen" },
  { name: "Consulta de Datos", href: "/consulta", icon: "Search" },
  { name: "Mapa de Contratos", href: "/mapa", icon: "MapPin" },
  { name: "Configuración", href: "/configuracion", icon: "Settings" },
];
