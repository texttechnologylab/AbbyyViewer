interface Node {
    getAttribute(attr: string): string;
    getElementsByTagName(attr: string): Array<Node>;
}