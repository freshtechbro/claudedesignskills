/**
 * PixiJS Starter Project
 * Main application initialization
 */

(async () => {
    // Create PixiJS application
    const app = new PIXI.Application();

    await app.init({
        width: window.innerWidth,
        height: window.innerHeight,
        backgroundColor: 0x1a1a2e,
        antialias: true,
        resolution: window.devicePixelRatio || 1,
        autoDensity: true
    });

    document.body.appendChild(app.canvas);

    // Create sprite container
    const spriteContainer = new PIXI.Container();
    app.stage.addChild(spriteContainer);

    // Sprite collection
    const sprites = [];

    // Create sprite texture
    function createSpriteTexture(color) {
        const graphics = new PIXI.Graphics();
        graphics.circle(25, 25, 25).fill(color);
        return app.renderer.generateTexture(graphics);
    }

    const textures = [
        createSpriteTexture(0xe74c3c),
        createSpriteTexture(0x3498db),
        createSpriteTexture(0x2ecc71),
        createSpriteTexture(0xf39c12),
        createSpriteTexture(0x9b59b6)
    ];

    // Add sprites function
    function addSprites(count = 10) {
        for (let i = 0; i < count; i++) {
            const texture = textures[Math.floor(Math.random() * textures.length)];
            const sprite = new PIXI.Sprite(texture);

            sprite.anchor.set(0.5);
            sprite.position.set(
                Math.random() * app.screen.width,
                Math.random() * app.screen.height
            );
            sprite.scale.set(Math.random() * 0.5 + 0.5);

            // Velocity
            sprite.vx = (Math.random() - 0.5) * 2;
            sprite.vy = (Math.random() - 0.5) * 2;

            // Interactive
            sprite.eventMode = 'static';
            sprite.cursor = 'pointer';

            sprite.on('pointerdown', () => {
                sprite.tint = Math.random() * 0xffffff;
            });

            spriteContainer.addChild(sprite);
            sprites.push(sprite);
        }

        updateSpriteCount();
    }

    // Clear sprites function
    function clearSprites() {
        sprites.forEach(sprite => sprite.destroy());
        sprites.length = 0;
        spriteContainer.removeChildren();
        updateSpriteCount();
    }

    // Update sprite count display
    function updateSpriteCount() {
        document.getElementById('sprite-count').textContent = sprites.length;
    }

    // Setup UI controls
    let statsVisible = true;

    document.getElementById('toggle-stats').addEventListener('click', () => {
        statsVisible = !statsVisible;
        document.getElementById('stats-panel').classList.toggle('hidden');
    });

    document.getElementById('add-sprites').addEventListener('click', () => {
        addSprites(20);
    });

    document.getElementById('clear-sprites').addEventListener('click', () => {
        clearSprites();
    });

    // Update loop
    app.ticker.add((ticker) => {
        // Move sprites
        sprites.forEach(sprite => {
            sprite.x += sprite.vx * ticker.deltaTime;
            sprite.y += sprite.vy * ticker.deltaTime;

            // Bounce off edges
            if (sprite.x < 0 || sprite.x > app.screen.width) {
                sprite.vx *= -1;
            }
            if (sprite.y < 0 || sprite.y > app.screen.height) {
                sprite.vy *= -1;
            }

            // Keep within bounds
            sprite.x = Math.max(0, Math.min(app.screen.width, sprite.x));
            sprite.y = Math.max(0, Math.min(app.screen.height, sprite.y));

            // Rotate
            sprite.rotation += 0.01 * ticker.deltaTime;
        });

        // Update stats
        if (statsVisible) {
            document.getElementById('fps').textContent = Math.round(app.ticker.FPS);
            document.getElementById('draw-calls').textContent = app.renderer.stats.drawCalls.total || 0;
        }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        app.renderer.resize(window.innerWidth, window.innerHeight);
    });

    // Initial sprites
    addSprites(50);

    console.log('PixiJS application initialized');
    console.log('Canvas size:', app.screen.width, 'x', app.screen.height);
    console.log('Resolution:', app.renderer.resolution);
})();
