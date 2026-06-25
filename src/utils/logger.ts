import { debugOptions } from "@config/debug";

export const logger = {
    routes(routes: string[]) {
        if(!debugOptions.DISPLAY_ROUTES) return;

        console.log("Generated routes:");
        console.table(routes);
    }
}