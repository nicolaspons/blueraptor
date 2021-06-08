var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 600,
  height: 300,
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
  upColor: 'rgba(0, 255, 0, 1)',
  downColor: '#000',
  borderDownColor: 'rgba(255, 144, 0, 1)',
  borderUpColor: 'rgba(255, 144, 0, 1)',
  wickDownColor: 'rgba(255, 144, 0, 1)',
  wickUpColor: 'rgba(255, 144, 0, 1)',
});

fetch('http://localhost:5000/history')
	.then((r) => r.json())
	.then((response) => {
		candleSeries.setData(response)
		candleSeries.setMarkers(addMarkers(response))
	})

var binanceSocket = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@kline_15m')
binanceSocket.onmessage = (event) => {
	var message = JSON.parse(event.data)
	var candlestick = message.k
	candleSeries.update({
		time: candlestick.t / 1000,
		open: candlestick.o,
		high: candlestick.h,
		low: candlestick.l,
		close: candlestick.c
	})
}
function addMarkers(candlesticks) {
	var markers = []
	console.log(candlesticks)
	for (var i = 0; i < candlesticks.length; ++i) {
		if (candlesticks[i].close < 31500) {
			console.log(candlesticks[i])
			markers.push({
				time: candlesticks[i].time,
				position: 'belowBar',
				color: '#e91e63',
				shape: 'arrowUp',
				text: 'Buy @ ' + Math.floor(candlesticks[i].close)
			});
		}
	}
	return markers
}