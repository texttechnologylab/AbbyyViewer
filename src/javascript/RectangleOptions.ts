export class RectangleOptions {

    top: number
    left: number
    height: number
    width: number
    xml: Node

    constructor(xmlBlock: Node){
        const t = Number(xmlBlock.getAttribute("t"))
        const b = Number(xmlBlock.getAttribute("b"))
        const l = Number(xmlBlock.getAttribute("l"))
        const r = Number(xmlBlock.getAttribute("r"))

        this.top = t
        this.left = l
        this.height = b-t
        this.width = r-l

        this.xml = xmlBlock
    }

}