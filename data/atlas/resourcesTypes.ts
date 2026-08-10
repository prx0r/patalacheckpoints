// The Tantra Hub external-resources register.
// One URL can be useful in several ways, so a resource carries multiple `types`
// and multiple `traditions`. The register is a federation/join layer: we index
// and deep-link resources rather than rehosting them (several explicitly forbid
// reposting; a few are non-public-domain — see `can_rehost` / `rights`).

export type ResourceType =
  | "primary_text"
  | "manuscript"
  | "manuscript_catalogue"
  | "translation"
  | "scholarship"
  | "traditional_teaching"
  | "lecture"
  | "oral_transmission"
  | "legacy_archive"
  | "sanskrit_tool"
  | "electronic_text"
  | "mirror"
  | "reference"
  | "discovery"
  | "critical_edition"
  | "bibliography"
  | "academic_project"
  | "mailing_list"
  | "manuscript_locator"
  | "text_reader"
  | "commentary";

export type Tradition =
  | "Trika"
  | "Krama"
  | "Kubjikā"
  | "Kaula"
  | "Siddhānta"
  | "Śrīvidyā"
  | "Śākta"
  | "Pratyabhijñā"
  | "Spanda"
  | "Vidyāpīṭha"
  | "Sarvāmnāya"
  | "Kālīkula"
  | "general";

export type Access = "free" | "mixed" | "paid" | "free_donation";

// PUBLIC/VERIFIED vs DISCOVERY (needs individual review) — the statuses from the
// resource survey. DISCOVERY resources belong in an internal crawler queue rather
// than being published as authoritative.
export type ResourceStatus = "public" | "discovery";

export interface ResourceLink {
  url: string;
  label?: string;
}

export interface Resource {
  id: string;
  name: string;
  url?: string;
  links?: ResourceLink[];
  types: ResourceType[];
  traditions: Tradition[];
  access: Access;
  machine_readable: boolean;
  can_rehost: boolean;
  rights?: "open" | "public_domain" | "permission" | "restricted" | "mixed" | "unknown";
  status: ResourceStatus;
  essential?: boolean;
  note: string;
  // Optional per-resource curated links to specific texts/works — the contextual
  // join layer (e.g. Mahānaya → Kramasadbhāva →).
  works?: ResourceLink[];
}

// Type labels shown in the UI filter.
export const TYPE_LABEL: Record<ResourceType, string> = {
  primary_text: "Primary text",
  manuscript: "Manuscript",
  manuscript_catalogue: "Manuscript catalogue",
  translation: "Translation",
  scholarship: "Scholarship",
  traditional_teaching: "Traditional teaching",
  lecture: "Lecture",
  oral_transmission: "Oral transmission",
  legacy_archive: "Legacy archive",
  sanskrit_tool: "Sanskrit tool",
  electronic_text: "Electronic text",
  mirror: "Mirror",
  reference: "Reference",
  discovery: "Discovery",
  critical_edition: "Critical edition",
  bibliography: "Bibliography",
  academic_project: "Academic project",
  mailing_list: "Mailing list",
  manuscript_locator: "Manuscript locator",
  text_reader: "Text reader",
  commentary: "Commentary",
};
