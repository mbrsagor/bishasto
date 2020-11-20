import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Route | item/nutration', function(hooks) {
  setupTest(hooks);

  test('it exists', function(assert) {
    let route = this.owner.lookup('route:item/nutration');
    assert.ok(route);
  });
});
