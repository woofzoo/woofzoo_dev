import {
  BarChart3,
  Calendar,
  CreditCard,
  FileText,
  Heart,
  History,
  Home,
  List,
  LucideIcon,
  Package,
  PlusCircle,
  Settings,
  Stethoscope,
  UserCheck,
  Users,
} from "lucide-react";

interface SubItem {
  id: string;
  label: string;
  icon: LucideIcon;
}

interface MenuItem {
  id: string;
  label: string;
  icon: LucideIcon;
  description: string;
  expandable?: boolean;
  subItems?: SubItem[];
}

export const menuItems: MenuItem[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: Home,
    description: "Overview & alerts",
  },
  {
    id: "patients",
    label: "Patients (Pets)",
    icon: Heart,
    description: "Pet management",
    expandable: true,
    subItems: [
      { id: "patients-list", label: "List View", icon: List },
      { id: "patients-history", label: "Medical History", icon: History },
      { id: "patients-add", label: "Add New Pet", icon: PlusCircle },
    ],
  },
  {
    id: "owners",
    label: "Pet Owners",
    icon: Users,
    description: "Owner details & accounts",
  },
  {
    id: "medical",
    label: "Medical Records",
    icon: FileText,
    description: "Health records",
    expandable: true,
    subItems: [
      { id: "appointments", label: "Appointments", icon: Calendar },
      { id: "medical-vaccinations", label: "Vaccinations", icon: Stethoscope },
      { id: "medical-surgeries", label: "Surgeries", icon: FileText },
      { id: "medical-allergies", label: "Allergies", icon: FileText },
      { id: "medical-prescriptions", label: "Prescriptions", icon: FileText },
    ],
  },
  {
    id: "inventory",
    label: "Inventory",
    icon: Package,
    description: "Stock & supplies",
  },
  {
    id: "billing",
    label: "Billing & Payments",
    icon: CreditCard,
    description: "Invoices & reports",
  },
  {
    id: "staff",
    label: "Staff Management",
    icon: UserCheck,
    description: "Team & schedules",
  },
  {
    id: "reports",
    label: "Reports & Analytics",
    icon: BarChart3,
    description: "Business insights",
  },
  {
    id: "settings",
    label: "Settings",
    icon: Settings,
    description: "Clinic configuration",
  },
];
