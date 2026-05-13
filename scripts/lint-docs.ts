import * as fs from 'fs';
import { parse } from '@stoplight/yaml';

const spec = parse(fs.readFileSync('./reference/openapi.yaml', 'utf8')) as any;
let errorCount = 0;

console.log("--- Documentation Quality Audit ---");

const paths = spec.paths;

for (const path in paths) {
    for (const method in paths[path]) {
        const op = paths[path][method];

        if (!op.summary) {
            console.error(`MISSING SUMMARY: ${method.toUpperCase()} ${path}`);
            errorCount++;
        }

        if (op.description && !op.description.endsWith('.')) {
            console.error(`STYLE ERROR: Description for ${path} should end with a period.`);
            errorCount++;
        }

        const MIN_DEFINITION_LENGTH = 10;
        const description = op.description || "";
        const wordCount = description.split(' ').length;

        if (wordCount < MIN_DEFINITION_LENGTH) {
            console.warn(`STYLE WARNING: ${method.toUpperCase()} ${path}`);
            console.warn(`   Description is too short (${wordCount} words). Please expand.`);
        }
    }
}

if (errorCount > 0) {
    console.log(`\nFound ${errorCount} documentation issues. Fix them to pass the build.`);
    process.exit(1);
} else {
    console.log("\nAll documentation standards met!");
    process.exit(0);
}
