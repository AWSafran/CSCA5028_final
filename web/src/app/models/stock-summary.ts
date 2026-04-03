import { ObjectId } from "./object-id";
import { Stock } from "./stock";

export interface StockSummary {
    _id?: ObjectId;
    fecth_date?: string;
    percent_min?: Stock[];
    percent_max?: Stock[];
    nominal_min?: Stock[];
    nominal_max?: Stock[];
}