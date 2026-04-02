import { ObjectId } from "./object-id"

export interface stock {
    T?: string,
    _id?: ObjectId
    c?: number;
    delta?: number;
    delta_pct?: number;
    fetch_date?: string;
    h?: number;
    l?: number;
    n?: number;
    o?: number;
    t?: number;
    v?: number;
    vw?: number;
}