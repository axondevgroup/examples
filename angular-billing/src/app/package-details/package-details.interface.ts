export interface PackageDetails {
  package_code: string;
  package_id: number;

  rate: Rate;
  services: Services[];
  components: Components[];
}

interface Rate {
  amount: number;
  type: string;
}

interface Services {
  service_code: string;
  name: string;

  rate: Rate;
}

interface Components {
  component_code: string;
  name: string;

  rate: Rate;
}
