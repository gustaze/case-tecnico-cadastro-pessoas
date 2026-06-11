import "./App.css";
import { useState } from "react";

function App(){
  
  const [nome, setNome] = useState("");
  const [cpf, setCpf] = useState("");
  const [email, setEmail] = useState("");
  const [dataNascimento, setDataNascimento] = useState("");
  const [cep, setCep] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [pessoaCadastrada, setPessoaCadastrada] = useState(null);
  const [complemento, setComplemento] = useState("");
  const [logradouro, setLogradouro] = useState("");
  const [numeroEndereco, setNumeroEndereco] = useState("");
  const [bairro, setBairro] = useState("");
  const [cidade, setCidade] = useState("");
  const [uf, setUf] = useState("");
  const [tipoMensagem, setTipoMensagem] = useState("")
  const [carregandoCep, setCarregandoCep] = useState(false)
  const [cadastrando, setCadastrando] = useState(false)
  
  async function cadastrarPessoa(event) {
    event.preventDefault()

    if (!nome.trim()) {
      setMensagem("Nome é obrigatório")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if (!/^[A-Za-zÀ-ÿ ]+$/.test(nome.trim())) {
      setMensagem("Nome deve conter apenas letras e espaços")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if (cpf.replace(/\D/g, "").length !== 11) {
      setMensagem("CPF deve conter 11 números")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
    return
    }

    if (!email.trim()) {
      setMensagem("E-mail é obrigatório")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if(!email.includes("@") || !email.includes(".")){
      setMensagem("Informe um e-mail válido")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if (dataNascimento.replace(/\D/g, "").length !== 8) {
      setMensagem("Data de nascimento é obrigatória")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    const partesData = dataNascimento.split("/")
    const dataFormatada = `${partesData[2]}-${partesData[1]}-${partesData[0]}`

    const dataInformada = new Date(dataFormatada)
    const hoje = new Date()

    if(dataInformada > hoje){
      setMensagem("Data de nascimento não pode ser futura")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if (cep.replace(/\D/g, "").length !== 8) {
      setMensagem("CEP deve conter 8 números.")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if (!logradouro || !bairro || !cidade || !uf) {
      setMensagem("Informe um CEP válido para preencher o endereço")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    if (!numeroEndereco.trim()) {
      setMensagem("Número do endereço é obrigatório")
      setTipoMensagem("erro")
      setPessoaCadastrada(null)
      return
    }

    setCadastrando(true)

    try {
      const resposta = await fetch("http://127.0.0.1:8000/pessoas/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          nome: nome,
          cpf: cpf.replace(/\D/g, ""),
          email: email,
          data_nascimento: dataFormatada,
          cep: cep.replace(/\D/g, ""),
          numero_endereco: numeroEndereco,
          complemento: complemento
        })
      })

      const dados = await resposta.json()

      if (resposta.ok) {
          setCadastrando(false)
          setMensagem(dados.message)
          setTipoMensagem("sucesso")
          setPessoaCadastrada(dados)

          setNome("")
          setCpf("")
          setEmail("")
          setDataNascimento("")
          setCep("")
          setComplemento("")
          setNumeroEndereco("")

          setLogradouro("")
          setBairro("")
          setCidade("")
          setUf("")
          
      } else {
        
          setMensagem(dados.detail?.[0]?.msg || dados.detail || "Erro ao realizar cadastro")
          setTipoMensagem("erro")
          setPessoaCadastrada(null)
        }

    } catch (erro) {
      console.error("Erro ao chamar API:", erro)
      setMensagem("Erro ao conectar com a API.")
      setTipoMensagem("erro")
    } finally {
      setCadastrando(false)
    }
  }

  async function buscarCep(cepDigitado) {
    setCarregandoCep(true)

    try {
      const resposta = await fetch(
        `https://viacep.com.br/ws/${cepDigitado}/json/`
      )
    

      const dados = await resposta.json()
    
      if (dados.erro) {
        setMensagem("CEP não encontrado.")
        setTipoMensagem("erro")
        setLogradouro("")
        setBairro("")
        setCidade("")
        setUf("")
        return
      }

      setMensagem("")
      setLogradouro(dados.logradouro)
      setBairro(dados.bairro)
      setCidade(dados.localidade)
      setUf(dados.uf)
     } catch (erro) {
      setMensagem("Erro ao buscar CEP.")
      setTipoMensagem("erro")
    } finally {
      setCarregandoCep(false)
    }
  } 
  
  return(
    <div className="container">
      <h1>Cadastro de Pessoas</h1>

      <div className="card">
        <form onSubmit={cadastrarPessoa}>
          <div className="form-grid">
            <div className="form-group">
              <label>Nome</label>              
              <input type="text"
                placeholder="Nome Completo"
                value={nome}
                onChange={(e) => {
                  setMensagem("")
                  setNome(e.target.value)
                }}
              />
            </div>
          

            <div className="form-group">
              <label>CPF</label>
              <input type="text"
                placeholder="000.000.000-00"
                value={cpf}
                maxLength={14}
                onChange={(e) => {
                  setMensagem("")
                  let valor = e.target.value

                  valor = valor.replace(/\D/g, "")
                  valor = valor.slice(0, 11)

                  valor = valor.replace(
                    /(\d{3})(\d)/,
                    "$1.$2"
                  )
                  valor = valor.replace(
                    /(\d{3})(\d)/,
                    "$1.$2"
                  )

                  valor = valor.replace(
                    /(\d{3})(\d{1,2})$/,
                    "$1-$2"
                  )

                  setCpf(valor)
                }}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input type="text"
                placeholder="email@exemplo.com"
                value={email}
                onChange={(e) => {
                  setMensagem("")
                  setEmail(e.target.value)
                }}
              />
            </div>

            <div className="form-group">
              <label>Data de nascimento</label>
              <input type="text"
                placeholder="DD/MM/AAAA"
                value={dataNascimento}
                maxLength={10}
                onChange={(e) => {
                  setMensagem("")
                  let valor =e.target.value

                  valor = valor.replace(/\D/g, "")
                  valor = valor.slice(0, 8)

                  valor = valor.replace(/(\d{2})(\d)/, "$1/$2")
                  valor = valor.replace(/(\d{2})(\d)/, "$1/$2")

                  setDataNascimento(valor)
                }}
              />
            </div>

            <div className="form-group">
              <label>CEP</label>
              <input type="text"
                placeholder="00000-000"
                value={cep}
                maxLength={9}
                onChange={(e) => {
                  setMensagem("")
                  let valor = e.target.value
                  
                  valor = valor.replace(/\D/g, "")
                  valor = valor.slice(0, 8)

                  const cepLimpo = valor

                  valor = valor.replace(/(\d{5})(\d)/, "$1-$2")

                  setCep(valor)

                  if (cepLimpo.length === 8){
                    buscarCep(cepLimpo)
                  }    

                }}
              />
              {carregandoCep && (
                <span className="loading">
                  Buscando CEP...
                </span>
              )}
            </div>

            <div className="form-group">
              <label>Endereço</label>
              <input type="text" value={logradouro} readOnly />
            </div>

            <div className="form-group">
              <label>Número</label>
              <input type="text"
              value={numeroEndereco}
              onChange={(e) => {
                setMensagem("")
                setNumeroEndereco(e.target.value)
              }}
              />
            </div>

            <div className="form-group">
              <label>Complemento</label>
              <input type="text"
              value={complemento}
              onChange={(e) => {
                setMensagem("")
                setComplemento(e.target.value)
              }}
              />
            </div>

            <div className="form-group">
              <label>Bairro</label>
              <input type="text" value={bairro} readOnly />
            </div>

            <div className="form-group">
              <label>Cidade</label>
              <input type="text" value={cidade} readOnly />
            </div>

            <div className="form-group">
              <label>UF</label>
              <input type="text" value={uf} readOnly />
            </div>
          </div>
          <br/>
          <div className="form-actions">
            <button 
              type="submit"
              disabled={cadastrando}
            > 
              {cadastrando ? "Cadastrando..." : "Cadastrar"}
            </button>
          </div>
      </form>

      {mensagem && (
        <p className={`mensagem mensagem-${tipoMensagem}`}>
          {mensagem}  
        </p>
      )}

      {pessoaCadastrada && (
        <div className="resultado">
          <h3>Dados cadastrados</h3>

          <p><strong>Login:</strong> {pessoaCadastrada.login}</p>

          <p>
            <strong>Endereço:</strong> {pessoaCadastrada.logradouro},
            nº {" "}{pessoaCadastrada.numero_endereco}
          </p>

          <p>
            <strong>Complemento:</strong> {pessoaCadastrada.complemento}
          </p>

          <p>
            <strong>Cidade:</strong> {pessoaCadastrada.cidade}/{pessoaCadastrada.uf}
          </p>        
        </div>
      )}
    </div>
  </div>
  )
}

export default App