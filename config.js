const http = require('http')
            const port = process.env.PORT || 8086
            const websockify = require('@sukkis/node-multi-websockify')
            const server = http.createServer()
            server.listen(port)
            websockify(server, 
            [
                {target: '10.199.999.99:9000', path: '/S022033601'},
                ])