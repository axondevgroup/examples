export interface ComponentDetails {
  code: string;
  company_id: number;
  component_id: number;
  name: string;
  type: string;
  rates: Rates[];
}

interface Rates {
  amount: number;
  package_code: string;
  package_id: number;
  quota: number;
  type: string;
}
