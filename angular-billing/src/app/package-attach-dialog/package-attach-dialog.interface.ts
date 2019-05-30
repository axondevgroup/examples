import {ComponentList, ServicesList} from '../package-create/package-create.interface';

export interface PackageAttachDialog {
  title: string;
  selectList: ServicesList | ComponentList;
  type?: string;
  name?: string;
  formValues: FormValues;
}

interface FormValues {
  selectedName: string;
  type: string;
  quota: number;
  rate: number;
}
