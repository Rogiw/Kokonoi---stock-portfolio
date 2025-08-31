


//Tenho que relembrar esse java script



/*document.addEventListener('DOMContentLoaded', function() {
            const empresaInput = document.getElementById('empresaInput');
            const buscarBtn = document.getElementById('buscarBtn');
            const resultsContainer = document.getElementById('resultsContainer');
            const loadingElement = document.getElementById('loading');
            const messageElement = document.getElementById('message');
            
            buscarBtn.addEventListener('click', buscarEmpresa);
            empresaInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    buscarEmpresa();
                }
            });
            
            function buscarEmpresa() {
                const nomeEmpresa = empresaInput.value.trim();
                
                if (!nomeEmpresa) {
                    showMessage('Por favor, digite o nome de uma empresa.');
                    return;
                }
                
                loadingElement.style.display = 'block';
                messageElement.style.display = 'none';
                
                fetch(`/buscar_empresa?nome=${encodeURIComponent(nomeEmpresa)}`)
                    .then(response => response.json())
                    .then(data => {
                        loadingElement.style.display = 'none';
                        
                        if (data.erro) {
                            showMessage(data.erro);
                            return;
                        }
                        
                        if (data.mensagem) {
                            showMessage(data.mensagem);
                            return;
                        }
                        
                        displayResults(data);
                    })
                    .catch(error => {
                        loadingElement.style.display = 'none';
                        showMessage('Erro ao buscar informações. Tente novamente.');
                        console.error('Erro:', error);
                    });
            }
            
            function displayResults(empresas) {
                resultsContainer.innerHTML = '';
                
                if (empresas.length === 0) {
                    showMessage('Nenhuma empresa encontrada com esse nome.');
                    return;
                }
                
                empresas.forEach(empresa => {
                    const empresaCard = document.createElement('div');
                    empresaCard.className = 'empresa-card';
                    
                    empresaCard.innerHTML = `
                        <h2 class="empresa-nome">${empresa.nome}</h2>
                        <div class="empresa-info">
                            <div class="info-item">
                                <span class="info-label">CNPJ</span>
                                <span class="info-value">${empresa.cnpj}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Endereço</span>
                                <span class="info-value">${empresa.endereco}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Telefone</span>
                                <span class="info-value">${empresa.telefone}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">E-mail</span>
                                <span class="info-value">${empresa.email}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Ramo de Atividade</span>
                                <span class="info-value">${empresa.ramo}</span>
                            </div>
                        </div>
                    `;
                    
                    resultsContainer.appendChild(empresaCard);
                });
            }
            
            function showMessage(mensagem) {
                messageElement.innerHTML = `<p>${mensagem}</p>`;
                messageElement.style.display = 'block';
                resultsContainer.innerHTML = '';
                resultsContainer.appendChild(messageElement);
            }
        }); */