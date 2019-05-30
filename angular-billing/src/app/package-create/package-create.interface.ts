/**
 * Types list for included services dialog.
 */

export interface ServicesList {
  name: string;
  service_code: string;
}

/**
 * Types list for included components dialog.
 */

export interface ComponentList {
  name: string;
  code: string;
  rates: Rates[];
}

interface Rates {
  amount: number;
  type: string;
}

/**
 * Types list for attach new package to component or service.
 */

export interface AttachPackage {
  name: string;
  code: string;
  monthly_rate: number;
  package_id?: number;

  services: Service[];
  components: Component[];
}

interface Service {
  service_id?: number;
}

interface Component {
  component_id?: number;
  rate?: number;
  rate_type?: string;
  quota?: number;
  name?: string;
}

export interface AttachedPackage extends AttachPackage {
  service_code: string;
}
