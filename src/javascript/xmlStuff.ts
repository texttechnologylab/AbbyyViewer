export function formatXML(input: string, indent?:string|null) {
  indent = indent || '\t'; //you can set/define other ident than tabs


  //PART 1: Add \n where necessary
  var xmlString = input.replace(/^\s+|\s+$/g, '');  //trim it (just in case) {method trim() not working in IE8}

  xmlString = input
                   .replace( /(<([a-zA-Z]+\b)[^>]*>)(?!<\/\2>|[\w\s])/g, "$1\n" ) //add \n after tag if not followed by the closing tag of pair or text node
                   .replace( /(<\/[a-zA-Z]+[^>]*>)/g, "$1\n") //add \n after closing tag
                   .replace( />\s+(.+?)\s+<(?!\/)/g, ">\n$1\n<") //add \n between sets of angled brackets and text node between them
                   .replace( />(.+?)<([a-zA-Z])/g, ">\n$1\n<$2") //add \n between angled brackets and text node between them
                   .replace(/\?></, "?>\n<") //detect a header of XML


  var xmlArr = xmlString.split('\n');  //split it into an array (for analise each line separately)



  //PART 2: indent each line appropriately

  var tabs = '';  //store the current indentation
  var start = 0;  //starting line

  if (/^<[?]xml/.test(xmlArr[0]))  start++;  //if the first line is a header, ignore it

  for (var i = start; i < xmlArr.length; i++) //for each line
  {  
    var line = xmlArr[i].replace(/^\s+|\s+$/g, '');  //trim it (just in case)

    if (/^<[/]/.test(line))  //if the line is a closing tag
     {
      tabs = tabs.replace(indent, '');  //remove one indent from the store
      xmlArr[i] = tabs + line;  //add the tabs at the beginning of the line
     }
     else if (/<.*>.*<\/.*>|<.*[^>]\/>/.test(line))  //if the line contains an entire node
     {
      //leave the store as is
      xmlArr[i] = tabs + line; //add the tabs at the beginning of the line
     }
     else if (/<.*>/.test(line)) //if the line starts with an opening tag and does not contain an entire node
     {
      xmlArr[i] = tabs + line;  //add the tabs at the beginning of the line
      tabs += indent;  //and add one indent to the store
     }
     else  //if the line contain a text node
     {
      xmlArr[i] = tabs + line;  // add the tabs at the beginning of the line
     }
  }


  //PART 3: return formatted string (source)
  return  xmlArr.join('\n');  //rejoin the array to a string and return it
}
