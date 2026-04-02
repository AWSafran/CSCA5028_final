import { ObjectId } from "./object-id";
import { stock } from "./stock";

export interface StockSummary {
    _id?: ObjectId;
    fecth_date?: string;
    percent_min?: stock[];
    percent_max?: stock[];
    nominal_min?: stock[];
    nominal_max?: stock[];
}