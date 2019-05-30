export interface Packages {
  name: string;
  package_code: string;
  package_id: string;
  is_default: boolean;
  rate: Rate;
}

interface Rate {
  amount: number;
  type: string;
}