export interface Invoice {
  invoice_id: number;
  customer_name: string;
  period: string;
  due_date: string;
  outstanding: number;
  total: number;
  status: string;
}
