const fase = document.querySelector('#fase>h1')
const btImage = document.querySelector('[upimages]')
const textbt = document.querySelector('[upimages]>p')
const formImages = document.querySelector('#fileInput')
const segmentacao = document.getElementById('segmentacao')
const tela = document.querySelector('#overview')
let Files = []


// mostrar global confs
// segmentacao.addEventListener('mouseenter',abrir_confs_global)



// esconder global confs
// segmentacao.addEventListener('mouseleave',fechar_confs_global)



document.addEventListener('click', (E)=>{
    const isInside = tela.contains(E.target)
    const isPreviewImg = E.target.classList.contains('itengalery')

    if (!isInside && !isPreviewImg) {
        tela.style.display = 'none'
    }
})
document.addEventListener('keydown',(event) =>{
    if (event.key === 'Escape'){
        tela.style.display = 'none'
    }
})
btImage.addEventListener("click", () => formImages.click())

btImage.addEventListener("dragover", (e)=>{
    e.preventDefault();
    textbt.innerText = 'Solte Aqui'
})

btImage.addEventListener("dragleave", ()=>{
    textbt.innerText = 'Carregar as Imagens'
})

btImage.addEventListener('drop',(e)=>{
    e.preventDefault();
    openGalery(e.dataTransfer.files)
})

formImages.addEventListener('change',()=>{
    openGalery(formImages.files)
})

function overview(src){
    tela.style.display = 'block'
    const img = document.querySelector('#overview>img')
    img.src = src
    
}
function openGalery(files) {
    document.querySelector('#segmentacao').style.display = 'block'
    // Junta as imagens novas
    Files = [...Files, ...Array.from(files)]

    // Verifica se já existe galery
    let galery = document.querySelector('.galery')
    
    // Se não existir ainda, cria
    if (!galery) {
        galery = document.createElement('div')
        galery.classList.add('galery')
        btImage.style.display = 'none'
        fase.innerText = 'Pre-Processamento'

        // Evento DROP dentro da galery (arrastar mais imagens)
        galery.addEventListener("dragover", e => e.preventDefault())
        galery.addEventListener("drop", e => {
            e.preventDefault()
            openGalery(e.dataTransfer.files)
        })

        btImage.parentNode.appendChild(galery)
    }

    // botão "+"
    let plusBtn = galery.querySelector('.add-more')
    if (!plusBtn) {
        plusBtn = document.createElement('img')
        plusBtn.src = plusImgUrl
        plusBtn.classList.add('itengalery', 'add-more')
        plusBtn.addEventListener("click", ()=> formImages.click())
        galery.appendChild(plusBtn)
    }

    // Render
    galery.innerHTML = ""
    galery.appendChild(plusBtn)

    Files.forEach(file => {
        const img = document.createElement('img')
        img.src = URL.createObjectURL(file)
        img.classList.add('itengalery')
        galery.appendChild(img)
        img.addEventListener('click',()=>{
            overview(img.src)
        })
    })
}
