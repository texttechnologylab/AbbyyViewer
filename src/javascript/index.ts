import { RectangleOptions } from "./RectangleOptions"
import { Elements } from "./Elements"
import { formatXML } from "./xmlStuff"


function getPathFromEvent(e: Event): string{
  //@ts-ignore
  return URL.createObjectURL(event.target.files[0])
}


// event Listener
document.addEventListener('readystatechange', event => {

//@ts-ignore
  if (event.target.readyState === "interactive") {   //same as:  ..addEventListener("DOMContentLoaded".. and   jQuery.ready
    Elements.getOpenImageDiv().addEventListener("click", () => {
      Elements.getImageInput().click()
    })

    Elements.getImageInput().addEventListener("change", (event) => {
      const path = getPathFromEvent(event)
      const fakePath = Elements.getImageInput().value
      if([".tif", "tiff"].includes(fakePath.slice(fakePath.length-4))){
        Elements.getOpenImageDiv().style.display = "none";
        loadTiff(path)
      } else if ([".png", ".jpg", "jpeg"].includes(fakePath.slice(fakePath.length-4))) {
        loadImage(path);
      } else {
        alert("input is invalid");
        Elements.getImageInput().value = "";
        return
      }
    });

    Elements.getXmlInput().addEventListener("change", (event) => {
      const path = getPathFromEvent(event)
      const fakePath = Elements.getXmlInput().value
      if(path.length < 4 || fakePath.slice(fakePath.length-3) != "xml"){
        alert("input is invalid")
        Elements.getXmlInput().value = ""
        return
      }
      loadXml(path)
    })



    // tabbs
    //@ts-ignore
    new Tabby('[data-tabs]')



  }

  //@ts-ignore
  if (event.target.readyState === "complete") {}

});




function clearFields(){
  Elements.getXmlContent().innerHTML = ""
  Elements.getTextContent().innerHTML = ""

  // delete all block diffs
  while(1){
    var bs = document.getElementsByClassName("blockThing")
    if(bs.length == 0) break;
    //@ts-ignore
    (bs[0] as Element).parentNode.removeChild(bs[0])
  }

  // delete all character diffs
  while(1){
    var cbs = document.getElementsByClassName("cBlockThing")
    if(cbs.length == 0) break;
    //@ts-ignore
    (cbs[0] as Element).parentNode.removeChild(cbs[0])
  }
}

function getImage(path: string, block: (image:any)=>void){
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'arraybuffer';
  xhr.open('GET', path);
  xhr.onload = function (e) {
    block(xhr.response)
  };
  xhr.send();
}

function loadTiff(path: string){
  // delete previous created boxes and xml output
  clearFields()

  //@ts-ignore
  Tiff.initialize({TOTAL_MEMORY: 50 * 1024 * 1024})

  getImage(path, (image) => {

    // delete previous created canvas
    var css = document.getElementsByClassName("imageCanvas")
    //@ts-ignore
    if(css.length > 0) css[0].parentElement.removeChild(css[0])

    // create new canvas (image)
    //@ts-ignore
    var tiff = new Tiff({buffer: image});
    var canvas = tiff.toCanvas();
    canvas.classList.add("imageCanvas")
    canvas.style.zIndex="6" 
    Elements.getCanvasHolder().append(canvas);
  })
  
}

function loadImage(path: string) {
  clearFields();
  Elements.getOpenImageDiv().style.display = "none";

  // delete previous created canvas
  var css = document.getElementsByClassName("imageCanvas");
  //@ts-ignore
  if (css.length > 0) css[0].parentElement.removeChild(css[0]);

  // create new canvas (image)
  let canvas = document.createElement('canvas');
  let context = canvas.getContext('2d');
  let img = document.createElement("img");
  img.src = path;
  img.onload = function () {
    canvas.height = img.height;
    canvas.width = img.width;
    //@ts-ignore
    context.drawImage(img, 0, 0, img.width, img.height);
    //@ts-ignore
    window.URL.revokeObjectURL(this.src);
  };

  canvas.classList.add("imageCanvas");
  canvas.style.zIndex = "6";
  // @ts-ignore
  Elements.getCanvasHolder().append(canvas);
}



function getDiv(xPos: number, yPos: number, width: number, height: number, imageScaleFactor: number){
  var rect = document.createElement("div")
  rect.style.top = imageScaleFactor * xPos + "px"
  rect.style.left = imageScaleFactor * yPos + "px"
  rect.style.width = imageScaleFactor * width + "px"
  rect.style.height = imageScaleFactor * height + "px"
  return rect
}


function makeCRect(xPos: number, yPos: number, width: number, height: number, scaleFactor: number, xml: Node){

  // add character box
  const rect = getDiv(yPos, xPos, width, height, scaleFactor)
  rect.classList.add("cBlockThing")

  //@ts-ignore
  Elements.getCanvasHolder().appendChild(rect)

  // add functions to show popup dialog
  rect.addEventListener('mouseover', (event) => {
    const bP = Elements.getCharacterBlockPreview()

    // format xmlString
    let xmlString = (new XMLSerializer()).serializeToString(xml);
    const readyString = xmlString.replace(/ ([^=]+)=/g, "\n\t$1=").replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/ /g, '&nbsp;').replace(/\n/g,'<br />')
    //@ts-ignore
    bP.innerHTML = PR.prettyPrintOne(readyString)

    const bPRect = bP.getBoundingClientRect();
    const bPHeight = bPRect.bottom - bPRect.top

    const mouseLeft = event.pageX
    const mouseTop = event.pageY

    // calculate where the popup window is supposed to show up
    const notEnoughSpace = mouseTop + bPHeight > window.screen.height -50

    if(notEnoughSpace){
	    bP.style.top = mouseTop - 10 - bPHeight + "px"
	    bP.style.left = mouseLeft + 10 + "px"
    } else{
	    bP.style.top = mouseTop + 10 + "px"
	    bP.style.left = mouseLeft + 10 + "px"
    }
    bP.style.visibility = "visible"


  })
  rect.addEventListener('mouseout', () => {
    const bP = Elements.getCharacterBlockPreview()
    bP.style.visibility = "hidden"
  })
}

function makeRect(rectObj: RectangleOptions, realWidth: number, realHeight: number){
  const imageScaleFactor = calcScaleFactor(realWidth, realHeight)
  if(imageScaleFactor == null) return

  // create blockBox
  const rect = getDiv(rectObj.top, rectObj.left, rectObj.width, rectObj.height, imageScaleFactor)
  rect.classList.add("blockThing")
  rect.classList.add("blockThing-"+rectObj.xml.getAttribute("blockType"))

  // create inner character boxes
  const cXmls = rectObj.xml.getElementsByTagName("charParams")
  for(var i=0; i<cXmls.length; i++) {
    const co = cXmls[i]
    const t = Number(co.getAttribute("t"))
    const l = Number(co.getAttribute("l"))
    const b = Number(co.getAttribute("b"))
    const r = Number(co.getAttribute("r"))
    makeCRect(l, t, r-l, b-t, imageScaleFactor, co)
  }

  // set onClick Listener
  rect.onclick = () => {
    //alert("okr")
    const xmlString = (new XMLSerializer()).serializeToString(rectObj.xml);
    const readyString = formatXML(xmlString).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/ /g, '&nbsp;').replace(/\n/g,'<br />')

    Elements.getXmlContent().innerHTML = readyString


    new Promise((resolve, reject) => {
      //@ts-ignore
      Elements.getXmlContent().innerHTML = PR.prettyPrintOne(readyString)
    })



    Elements.getTextContent().innerHTML = getTextFromTextBlock(rectObj.xml)
  }

  rect.oncontextmenu = () => {
      const fakePath = Elements.getImageInput().value
      const regex = /.*\\(.*)\.(tif|tiff|png|jpg|jpeg")/
      //@ts-ignore
      const path = fakePath.match(regex)[1]
      if(path == null) {
	      alert("pfad konnte nicht gelesen werden")
	      return false
      } 
      const goldLine = path + ";" + rectObj.top + ";" + rectObj.left
      const inStandard = blockReplaceInGoldStandard(path, rectObj.top, rectObj.left)
      //alert(inStandard)
      //const value = inStandard ? 0 : 1;
      if(!inStandard) addLineToGoldStandard(path, rectObj.top, rectObj.left, 1)
      return false
  }



  //@ts-ignore
  Elements.getCanvasHolder().appendChild(rect)
  //rect.onClick = function(rectObj.content)

}


function getTextFromTextBlock(xmlBlock: Node){
  var text = ""
  var lBlocks = xmlBlock.getElementsByTagName("line")
  for(var j=0; j<lBlocks.length; j++){
    var lB = lBlocks[j]
    var cBlocks = lB.getElementsByTagName("charParams")
    for(var i=0; i<cBlocks.length; i++){
      var cB = cBlocks[i]
      //@ts-ignore
      text += cB.innerHTML
    }
    text += "<br>"
  }
  //console.log(cBlocks)
  return text
}


const domPareser = new DOMParser()
function openXmlFile(path: string, block: any){
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", path, true);
  rawFile.onreadystatechange = function() {
    if (rawFile.readyState === 4) {
      	var allText = rawFile.responseText;
      	var xml = domPareser.parseFromString( allText, "application/xml" )
	block(xml)
    }
  }
  rawFile.send();
}


function loadXml(path: string){
  openXmlFile(path, (xml: any) => {

	// delete previous created boxes and xml output
	clearFields()

	var page = xml.getElementsByTagName("page")[0]
	var realWidth = Number(page.getAttribute("width"))
	var realHeight = Number(page.getAttribute("height"))

	// create boxes
	var tags = xml.getElementsByTagName("block")
	for(var i=0; i < tags.length; i++){
		//@ts-ignore
		var rectObj = new RectangleOptions(tags[i])
		makeRect(rectObj, realWidth, realHeight)
	}

  })
}

// divide width of canvas through real width of image
function calcScaleFactor(realWidth: number, realHeight: number): number|null{

  // var image = Elements.getImageSide()
  var image = document.getElementsByClassName("imageCanvas")[0]
  if(image == null) return null
  var rect = image.getBoundingClientRect();
  var height = rect.bottom - rect.top;
  var width = rect.right - rect.left;
  //var realHeight = image.naturalHeight
  //var realWidth = image.naturalWidth

  //console.log("image height: " + height)
  //console.log("natural height: " + realHeight)

  return width / realWidth
}

function addLineToGoldStandard(pageNumber: string, top: number, left: number, value: number){
	const line = pageNumber + ";" + left + ";" + top + ";" + value + "\n"
	Elements.getGoldContent().value += line
}

function blockReplaceInGoldStandard(pageNumber: string, top: number, left: number){
	const lines = Elements.getGoldContent().value.split("\n")
	for(let i=0; i<lines.length; i++){
		const regex = "^"+ pageNumber +";"+ left +";"+ top +";(.*)$"
		let line = lines[i]
		if(line == "") continue
		const match = line.match(regex)
		if(match == null) continue
		// found matching line
		const value = match[1]
		const newValue = value == "1" ? 0 : 1
		line = line.substring(0, line.length - 1) + newValue
		lines[i] = line
		Elements.getGoldContent().value = lines.join("\n")
		return true
	}
	return false;
}
