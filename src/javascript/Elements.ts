export class Elements {

    static getImageInput(): HTMLInputElement{
        return document.getElementById("file-input") as HTMLInputElement
    }

    static getXmlInput(): HTMLInputElement{
        return document.getElementById("file-input-xml") as HTMLInputElement
    }


    static getImageSide(): HTMLElement{
        return document.getElementById("imageSide") as HTMLElement
    }

    static getOpenImageDiv(): HTMLElement{
        return document.getElementById("openImageDiv") as HTMLElement
    }

    static getCanvasHolder(): HTMLElement{
        return document.getElementById("canvasHolder") as HTMLElement
    }

    static getXmlSide(): HTMLElement{
        return document.getElementById("xmlSide") as HTMLElement
    }

    static getXmlContent(): HTMLPreElement{
        return document.getElementById("xmlContent") as HTMLPreElement
    }

    static getTextContent(): HTMLElement{
        return document.getElementById("textContent") as HTMLElement
    }



    static getCharacterBlockPreview(): HTMLElement{
        return document.getElementById("characterBlockPreview") as HTMLElement
    }

    
}