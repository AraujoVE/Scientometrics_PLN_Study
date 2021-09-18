const {Builder, By, Key, util, WebElement} = require("selenium-webdriver")
const { elementIsNotSelected } = require("selenium-webdriver/lib/until");
const fs = require('fs');
let rawdata = fs.readFileSync('./useds.json');
//let rweb = JSON.parse(rawdata);
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////           Generic Methods           ///////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

// Used to wait some time in seconds
async function wait(timeInSeconds){
    await new Promise(resolve => setTimeout(resolve, 1000*timeInSeconds));
}    

////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////           Page Methods           /////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////

//Get a new driver
async function getDriver(){
    return await new Builder().forBrowser("firefox").build();
}

//Maximize current window
async function maximizeWindow(driver){ //Maximize window
    await driver.manage().window().maximize();
}

//Go to 'pagePath' webpage
async function goToPage(driver,pagePath){
    await driver.get(pagePath);
}

//Open new window and goes to that window, if 'returnCurWindow=true' it returns current window
async function openWindow(driver,newWindowUrl,waitTime=0,returnCurWindow=false){
    await driver.executeScript('window.open("' + newWindowUrl + '");');
    
    let windows = await driver.getAllWindowHandles();
    await driver.switchTo().window(windows[windows.length - 1]);

    await wait(waitTime);
    if (returnCurWindow){
        return windows[windows.length - 2]
    }
}

//Close current window and go to passed window, or previous one, if no window is passed
async function closeWindow(driver,waitTime=0,nextWindow=null){ 
    await driver.close();
    let windows = await driver.getAllWindowHandles();
    let toGoWindow = (nextWindow === null ? windows[windows.length - 1] : nextWindow);
    await driver.switchTo().window(toGoWindow);
    await wait(waitTime);
}


///////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////           Basic Methods           ////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

//Used to type
async function typeSlowly(driver,string,xpathStr,waitTimeKey,waitTimeEnd){
    for(const key of string){
        await driver.findElement(By.xpath(xpathStr)).sendKeys(key);
        await wait(waitTimeKey);
    }    
    await wait(waitTimeEnd);
}     

//Used to click
async function clickXPath(driver,vars,waitTime=0){
    let xPathStr = vars[0];
    await driver.findElement(By.xpath(xPathStr)).click();
    await wait(waitTime);
    return true;
}    

//Used to get element
async function getElement(driver,vars,waitTime=0){
    let xPathStr = vars[0];
    let element = await driver.findElement(By.xpath(xPathStr));
    await wait(waitTime);
    return element
}    

//Used to get elements array
async function getElements(driver,vars,waitTime=0){
    let xPathStr = vars[0];
    let elements = await driver.findElements(By.xpath(xPathStr));
    await wait(waitTime);
    return elements
}        

//Used to get element attribute
async function getElemAttr(driver,vars,waitTime=0){
    let xPathStr = vars[0], attributeType = vars[1];
    var element = await getElement(driver,vars);
    var attribute = await element.getAttribute(attributeType);
    await wait(waitTime);
    return attribute;
}

//Used to get given attribute of many elements
async function getElemsAttr(driver,vars,waitTime=0){
    let xPathStr = vars[0], attributeType = vars[1];
    var elemAttrs = await getElements(driver,vars);

    for(i = 0;i<elemAttrs.length;i++){
        elemAttrs[i] = await elemAttrs[i].getAttribute(attributeType);
    }
    await wait(waitTime);
    return elemAttrs;
}



///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////           General Methods           ///////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

//To make action or return error, otherwise
async function xPathTryCatch(driver,funct,vars,errorMessage,waitTime=0){
    let returnVal = false;
    try{
        returnVal = await funct(driver,vars);
    }
    catch(error){
        returnVal = false;
    }
    await wait(waitTime);
    return returnVal;
}

//To try getting element until satisfied or maxRepts is reach 
async function xPathWhileTrue(driver,funct,vars,waitTime=0,waitBetween=0.5,maxRepts=1000){
    var continueWhile = true;
    var returnVal = false;
    let iter = 0;
    while(continueWhile === true){
        continueWhile = false;
        try{
            returnVal = await funct(driver,vars);
            continueWhile =  false;
        }    
        catch{
            returnVal = false;
            continueWhile =  (iter === maxRepts ? false : true);
            await wait(waitBetween);
        }
        iter++;    
    }
    await wait(waitTime);
    return returnVal;
}


////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////           Code           /////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////

/* 
This code is used to get all the texts from all first level
sub-areas of all science areas given by the wikipedia.
*/
async function writeFile(fileName,content){ //Write json file
    fs.writeFile(fileName,content, function (err) {
        if (err) {
            return console.log(err);
        }
        console.log("File ("+ fileName +") Writen");
    });
}

async function appendFile(fileName,content){ //Write json file
    fs.appendFile(fileName,"\n"+content, function (err) {
        if (err) {
            return console.log(err);
        }
        console.log("File ("+ fileName +") Writen");
    });
}

async function getText(driver,windowPath){
    let xPaths = [
        "//p[following-sibling::h2[contains(.,'See also')]]",
        "//p[following-sibling::h2[contains(.,'Notes')]]",
        "//p[following-sibling::h2[contains(.,'Footnotes')]]",
        "//p[following-sibling::h2[contains(.,'References')]]",
        "//p[following-sibling::h2[contains(.,'Bibliography')]]",
        "//p[following-sibling::h2[contains(.,'Major references')]]",
        "//p[following-sibling::h2[contains(.,'External links')]]",        
        "//div[@class='mw-parser-output']/p"
    ]
    await openWindow(driver,windowPath);
    await xPathWhileTrue(driver,getElement,["//p[following-sibling::h2]"]);
    await wait(1);
    let returnVal;
    for(xPath of xPaths){
        returnVal = (await getElemsAttr(driver,[xPath,"innerText"])).join("\n").trim();
        if(returnVal.length !== 0){
            console.log("\n"+xPath);
            break;
        }
    }
    if(returnVal.length === 0){
        driver.quit();
        throw new Error("paragraphs not found");
    }
    await closeWindow(driver);
    return returnVal + "\n";
}

async function main(){
    const driver = await getDriver();
    await goToPage(driver,"https://en.wikipedia.org/wiki/Outline_of_academic_disciplines");
    await maximizeWindow(driver);
    let scienceAreasIds = await getElemsAttr(driver,["//h3/span[@class='mw-headline']","id"]);
    let curXPathDiv,curXPathUl, subTopics, nameParts;
    let topicText = {};
    let mainWebsites;
    let webName;
    let gottenText;
    let jsonWebsites = {}
    console.log("SAIds:",scienceAreasIds);
    await fs.rmdirSync("./Texts",{recursive:true});
    await fs.mkdirSync("./Texts");
    for(let i = 0;i<scienceAreasIds.length;i++){
        let dirPath = "./Texts/"+scienceAreasIds[i];
        await fs.mkdirSync(dirPath);
        if(i === scienceAreasIds.length - 1){
            curXPathDiv = "//div[preceding-sibling::h3[./span[@id='"+ scienceAreasIds[i]+"']] and following-sibling::h2[contains(.,'See also')] and @class='div-col']/ul/li/a[1]";
            curXPathUl = "//ul[preceding-sibling::h3[./span[@id='"+ scienceAreasIds[i]+"']] and following-sibling::h2[contains(.,'See also')]]/li/a[1]";
        }
        else{
            curXPathDiv = "//div[preceding-sibling::h3[./span[@id='"+ scienceAreasIds[i]+"']] and following-sibling::h3[./span[@id='"+ scienceAreasIds[i+1]+"']] and @class='div-col']/ul/li/a[1]";
            curXPathUl = "//ul[preceding-sibling::h3[./span[@id='"+ scienceAreasIds[i]+"']] and following-sibling::h3[./span[@id='"+ scienceAreasIds[i+1]+"']]]/li/a[1]";
        }
        await xPathWhileTrue(driver,getElement,["//div"]);
        subTopics = await getElemsAttr(driver,[curXPathDiv,'href']);
        subTopics = subTopics.concat(await getElemsAttr(driver,[curXPathUl,'href']));
        console.log(scienceAreasIds[i]+":");

        topicText[scienceAreasIds[i]] = {};
        mainWebsites = [];
        for(let j = 0;j<subTopics.length;j++){
            nameParts = subTopics[j].split("/");
            webName = subTopics[j].split("#")[0];
            if(!mainWebsites.includes(webName)){
                mainWebsites.push(webName);
                gottenText = await getText(driver,webName);
                await writeFile((dirPath+"/"+nameParts[nameParts.length - 1]+".txt"),gottenText);
                //topicText[scienceAreasIds[i]][nameParts[nameParts.length - 1]] = gottenText;
                console.log("\t"+nameParts[nameParts.length - 1]+" : Read\n\t\t" + gottenText.substr(0,Math.min(10,gottenText.length-1))+"...");    
            }
            else{
                console.log("\t"+nameParts[nameParts.length - 1]+" : Not Read");
            }
        }
        jsonWebsites[scienceAreasIds[i]] = mainWebsites;
        //await writeFile(("./Texts/"+scienceAreasIds[i]+".txt"),topicText[scienceAreasIds[i]]);
        await writeFile("./useds.json",JSON.stringify(jsonWebsites));
    }
    await writeFile("./useds.json",JSON.stringify(jsonWebsites));
    driver.quit();
}
//main();
async function main2(){
    let usedJsons = await JSON.parse(rawdata);
    const driver = await getDriver();
    await goToPage(driver,"https://en.wikipedia.org/wiki/Outline_of_academic_disciplines");
    await maximizeWindow(driver);
    let filesPaths = {};
    let websitePath, appendFilePath,content,websiteName;
    let nameWebsites = [
        //And values not taken
        ['https://en.wikipedia.org/wiki/Political_philosophy','Philosophy'],
        ['https://en.wikipedia.org/wiki/Descriptive_ethics','Psychology'],
        ['https://en.wikipedia.org/wiki/High_availability','Computer_science'],
        ['https://en.wikipedia.org/wiki/Foundations_of_mathematics','Mathematics'],
        ['https://en.wikipedia.org/wiki/Topology','Mathematics'],
        ['https://en.wikipedia.org/wiki/Dietitian','Medicine_and_health'],
        // '/' values not taken
        ['https://en.wikipedia.org/wiki/Urban_sociology','Sociology'],
        ['https://en.wikipedia.org/wiki/Criminal_justice','Sociology'],
        ['https://en.wikipedia.org/wiki/Ethnic_studies','Sociology'],
        ['https://en.wikipedia.org/wiki/Population','Sociology'],
        ['https://en.wikipedia.org/wiki/Science_and_technology_studies','Sociology'],
        ['https://en.wikipedia.org/wiki/Rural_sociology','Sociology'],
        ['https://en.wikipedia.org/wiki/Clinical_pathology','Medicine_and_health'],
        ['https://en.wikipedia.org/wiki/Medical_laboratory','Medicine_and_health'],
        ['https://en.wikipedia.org/wiki/Health_informatics','Medicine_and_health']
    ];
    let jsonStr;
    for(let name of nameWebsites){
        websitePath = name[0].split("#")[0];
        websiteName = websitePath.split("/");
        appendFilePath = name[1];
        if(!usedJsons[appendFilePath].includes(websitePath)){
            console.log(websiteName[websiteName.length-1]+" sent to (./Texts/"+appendFilePath+".txt)");
            content = await getText(driver,websitePath);
            await writeFile("./Texts/"+appendFilePath+"/"+websiteName+".txt",content);
            //filesPaths[appendFilePath] = (appendFilePath in filesPaths ? (filesPaths[appendFilePath]+content) : content);
            usedJsons[appendFilePath].push(websitePath);
        }
        else{
            console.log(websiteName[websiteName.length-1]+" NOT sent to (./Texts/"+appendFilePath+".txt)");
            
        }
    }
    //for(key in filesPaths) await appendFile(("./Texts/"+key+".txt"),filesPaths[key]);
    jsonStr = await JSON.stringify(usedJsons);
    await writeFile("useds.json",jsonStr);
    driver.quit();

}

//main2("https://en.wikipedia.org/wiki/Political_philosophy");
main2();
//main();